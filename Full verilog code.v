`timescale 1ns/1ps

// i2c address translator
// us = upstream (acts as slave to master), ds = downstream (acts as master to slaves)

module i2c_address_translator #(
  parameter logic [6:0] UP_ADDR = 7'h49,
  parameter logic [6:0] DW_ADDR = 7'h48,
  parameter int PRESCALE = 250   // 50MHz -> ~100kHz*2
)(
  input  logic clk,
  input  logic rst,

  // upstream (slave side)
  input  logic us_scl_i,
  input  logic us_sda_i,
  output logic us_sda_o,
  output logic us_sda_oe,
  output logic us_scl_o,
  output logic us_scl_oe,

  // downstream (master side)
  input  logic ds_sda_i,
  output logic ds_scl_o,
  output logic ds_scl_oe,
  output logic ds_sda_o,
  output logic ds_sda_oe
);

  // sync to clk
  logic [1:0] us_scl_sync, us_sda_sync;
  always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
      us_scl_sync <= 2'b11;
      us_sda_sync <= 2'b11;
    end else begin
      us_scl_sync <= {us_scl_sync[0], us_scl_i};
      us_sda_sync <= {us_sda_sync[0], us_sda_i};
    end
  end

  logic us_scl, us_sda;
  assign us_scl = us_scl_sync[1];
  assign us_sda = us_sda_sync[1];

  // start/stop
  logic us_sda_q;
  always_ff @(posedge clk) us_sda_q <= us_sda;
  wire start_det = ( us_sda_q && !us_sda && us_scl);
  wire stop_det  = (!us_sda_q &&  us_sda && us_scl);

  // upstream open-drain
  logic us_sda_oe_r;
  assign us_sda_o  = 1'b0;
  assign us_scl_o  = 1'b1;
  assign us_scl_oe = 1'b0;
  assign us_sda_oe = us_sda_oe_r;

  // ds clock ~100kHz
  logic [15:0] div;
  logic scl_en, scl_en_q;
  always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
      div   <= '0;
      scl_en <= 1'b0;
    end else if (div == PRESCALE-1) begin
      div   <= '0;
      scl_en <= ~scl_en;
    end else begin
      div   <= div + 16'd1;
    end
  end
  always_ff @(posedge clk) scl_en_q <= scl_en;
  wire scl_rise =  scl_en & ~scl_en_q;
  wire scl_fall = ~scl_en &  scl_en_q;

  // upstream fsm
  typedef enum logic [2:0] { U_IDLE, U_ADDR, U_ACK, U_DATA, U_STOP } ustate_t;
  ustate_t ustate;

  logic [7:0] u_shift, u_byte;
  logic [2:0] u_bitcnt;
  logic u_rw, translating, u_ack;

  logic us_scl_q;
  always_ff @(posedge clk) us_scl_q <= us_scl;

  // kick ds once we ack addr
  logic ds_kick;
  always_ff @(posedge clk or posedge rst) begin
    if (rst)          ds_kick <= 1'b0;
    else if (ustate==U_ACK && translating) ds_kick <= 1'b1;
    else if (dstate==D_START)              ds_kick <= 1'b0;
  end

  always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
      ustate       <= U_IDLE;
      us_sda_oe_r  <= 1'b0;
      u_bitcnt     <= '0;
      translating  <= 1'b0;
      u_ack        <= 1'b0;
      u_rw         <= 1'b0;
      u_shift      <= '0;
      u_byte       <= '0;
    end else begin
      case (ustate)
        U_IDLE: begin
          us_sda_oe_r <= 1'b0;
          u_bitcnt    <= '0;
          if (start_det) ustate <= U_ADDR;
        end

        U_ADDR: begin
          if (!us_scl_q && us_scl) begin
            u_shift <= {u_shift[6:0], us_sda};
            u_bitcnt <= u_bitcnt + 3'd1;
            if (u_bitcnt == 3'd7) begin
              u_rw <= us_sda;
              if (u_shift[6:0] == UP_ADDR) begin
                translating <= 1'b1;
                ustate <= U_ACK;
              end else begin
                translating <= 1'b0;
                ustate <= U_IDLE;
              end
            end
          end
        end

        U_ACK: begin
          us_sda_oe_r <= translating; // pull low if we own it
          if (us_scl_q && !us_scl) begin
            us_sda_oe_r <= 1'b0;
            ustate <= translating ? U_DATA : U_IDLE;
          end
        end

        U_DATA: begin
          if (!u_rw) begin
            // master->us write: capture byte, ack each
            if (!us_scl_q && us_scl) begin
              u_byte   <= {u_byte[6:0], us_sda};
              u_bitcnt <= u_bitcnt + 3'd1;
              if (u_bitcnt == 3'd7) u_ack <= 1'b1;
            end
            if (u_ack && us_scl_q && !us_scl) us_sda_oe_r <= 1'b1; // ack low
            if (u_ack && !us_scl_q && us_scl) begin
              us_sda_oe_r <= 1'b0;
              u_ack <= 1'b0;
              u_bitcnt <= '0;
            end
          end else begin
            // read path placeholder (not wired through here)
            if (!us_scl_q && us_scl) us_sda_oe_r <= 1'b1;
            if ( us_scl_q && !us_scl) us_sda_oe_r <= 1'b0;
          end
          if (stop_det) ustate <= U_STOP;
          if (start_det) ustate <= U_ADDR;
        end

        U_STOP: begin
          translating <= 1'b0;
          us_sda_oe_r <= 1'b0;
          ustate <= U_IDLE;
        end
      endcase
    end
  end

  // downstream fsm (simple, write path)
  typedef enum logic [2:0] { D_IDLE, D_START, D_ADDR, D_ACK, D_DATA, D_ACK_H, D_STOP } dstate_t;
  dstate_t dstate;
  logic [7:0] d_shift, d_in;
  logic [2:0] d_bitcnt;

  logic ds_scl_q;
  always_ff @(posedge clk) ds_scl_q <= ds_scl_o;

  always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
      dstate    <= D_IDLE;
      ds_scl_o  <= 1'b1;
      ds_scl_oe <= 1'b0;
      ds_sda_o  <= 1'b1;
      ds_sda_oe <= 1'b0;
      d_bitcnt  <= '0;
      d_shift   <= '0;
      d_in      <= '0;
    end else if (translating) begin
      // push SCL out; keep it open-drain style (drive low on ~scl_en)
      ds_scl_o  <= 1'b0;
      ds_scl_oe <= ~scl_en;

      case (dstate)
        D_IDLE: begin
          ds_sda_o  <= 1'b1;
          ds_sda_oe <= 1'b0;
          d_bitcnt  <= '0;
          if (ds_kick && scl_en) dstate <= D_START;
        end

        D_START: begin
          if (scl_en) begin
            ds_sda_o  <= 1'b0;   // start
            ds_sda_oe <= 1'b1;
            d_shift   <= {DW_ADDR, u_rw};
            d_bitcnt  <= '0;
            dstate    <= D_ADDR;
          end
        end

        D_ADDR: begin
          if (scl_fall) begin
            ds_sda_o <= d_shift[7];
            d_shift  <= {d_shift[6:0], 1'b0};
            d_bitcnt <= d_bitcnt + 3'd1;
            if (d_bitcnt == 3'd7) dstate <= D_ACK;
          end
        end

        D_ACK: begin
          ds_sda_oe <= 1'b0; // release for slave ack
          if (scl_rise && ds_sda_i) dstate <= D_STOP; // nack -> stop
          if (scl_fall && !ds_sda_i) begin
            d_bitcnt <= '0;
            dstate   <= D_DATA;
          end
        end

        D_DATA: begin
          if (!u_rw) begin
            if (scl_fall) begin
              ds_sda_o <= d_shift[7];
              d_shift  <= {d_shift[6:0], 1'b0};
              d_bitcnt <= d_bitcnt + 3'd1;
              if (d_bitcnt == 3'd7) dstate <= D_ACK_H;
            end
          end else begin
            if (scl_fall) begin
              d_in    <= {d_in[6:0], ds_sda_i};
              d_bitcnt <= d_bitcnt + 3'd1;
              if (d_bitcnt == 3'd7) dstate <= D_ACK_H;
            end
          end
        end

        D_ACK_H: begin
          if (scl_fall) begin
            ds_sda_oe <= 1'b1; // ack low
            ds_sda_o  <= 1'b0;
          end
          if (scl_rise) begin
            ds_sda_oe <= 1'b0;
            d_bitcnt  <= '0;
            if (!u_rw) begin
              d_shift <= u_byte; // push next byte from upstream
              dstate  <= D_DATA;
            end else begin
              // read path handoff (not fully wired upstream)
              dstate <= D_DATA;
            end
          end
        end

        D_STOP: begin
          if (!scl_en) begin
            ds_sda_o  <= 1'b0;
            ds_sda_oe <= 1'b1;
          end else begin
            ds_sda_oe <= 1'b0; // stop
            dstate    <= D_IDLE;
          end
        end
      endcase
    end else begin
      ds_scl_o  <= 1'b1;
      ds_scl_oe <= 1'b0;
      ds_sda_o  <= 1'b1;
      ds_sda_oe <= 1'b0;
      dstate    <= D_IDLE;
    end
  end
endmodule

// very small i2c slave for sim sanity
module i2c_slave_model #(
  parameter logic [6:0] SLAVE_ADDR = 7'h48
)(
  input  logic clk,
  input  logic rst,
  input  logic scl,
  inout  tri   sda,
  output logic [7:0] reg_out
);
  // sync
  logic sda_d0, sda_d1;
  logic scl_d0, scl_d1;
  always_ff @(posedge clk) begin
    sda_d0 <= sda; sda_d1 <= sda_d0;
    scl_d0 <= scl; scl_d1 <= scl_d0;
  end
  wire sda_i = sda_d1;
  wire scl_i = scl_d1;

  // start/stop
  logic sda_q; always_ff @(posedge clk) sda_q <= sda_i;
  wire start_c = ( sda_q && !sda_i && scl_i);
  wire stop_c  = (!sda_q &&  sda_i && scl_i);

  // open drain
  logic sda_drv;
  assign sda = sda_drv ? 1'b0 : 1'bz;

  typedef enum logic [2:0] { S_IDLE, S_ADDR, S_ACK, S_DATA, S_DACK } sstate_t;
  sstate_t sstate;
  logic [7:0] sh;
  logic [2:0] bc;
  logic rw;

  logic scl_q; always_ff @(posedge clk) scl_q <= scl_i;

  always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
      sstate   <= S_IDLE;
      sda_drv  <= 1'b0;
      bc       <= '0;
      sh       <= '0;
      reg_out  <= '0;
      rw       <= 1'b0;
    end else begin
      if (start_c) begin
        sstate <= S_ADDR;
        bc <= '0; sh <= '0; sda_drv <= 1'b0;
      end

      if (!scl_q && scl_i) begin
        case (sstate)
          S_ADDR: begin
            sh <= {sh[6:0], sda_i};
            bc <= bc + 3'd1;
            if (bc == 3'd7) begin
              rw <= sda_i;
              if (sh[6:0] == SLAVE_ADDR) sstate <= S_ACK; else sstate <= S_IDLE;
            end
          end
          S_DATA: begin
            sh <= {sh[6:0], sda_i};
            bc <= bc + 3'd1;
            if (bc == 3'd7) begin
              reg_out <= {sh[6:0], sda_i};
              sstate <= S_DACK;
            end
          end
        endcase
      end

      if (scl_q && !scl_i) begin
        if (sstate==S_ACK || sstate==S_DACK) sda_drv <= 1'b1; // ack low
      end

      if (!scl_q && scl_i) begin
        if (sstate==S_ACK) begin
          sda_drv <= 1'b0;
          if (!rw) begin sstate <= S_DATA; bc <= '0; end
          else begin sstate <= S_IDLE; end
        end else if (sstate==S_DACK) begin
          sda_drv <= 1'b0; sstate <= S_DATA; bc <= '0;
        end
      end

      if (stop_c) begin
        sstate <= S_IDLE; sda_drv <= 1'b0; bc <= '0;
      end
    end
  end
endmodule