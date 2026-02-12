# FPGA Neural Processing Unit (NPU) — Quantized Activation Accelerator

A hardware neural compute primitive that performs fixed-point bias adjustment, rectified activation, and eight-bit quantization on streaming sixteen-bit signed inputs.  
The accelerator is validated against a software golden model and demonstrates deterministic correctness across randomized test vectors.

This repository presents a real-time neural inference datapath implemented directly in FPGA fabric using low-precision arithmetic and continuous streaming.

---

## Overview

Modern AI accelerators achieve performance and energy efficiency through quantized computation and nonlinear activation functions.  
This project implements the fundamental operation used in neural inference engines: bias-shifted activation followed by low-precision output projection.

The system continuously receives signed sixteen-bit values over a serial interface, transforms them in hardware, and returns compact eight-bit activations with no floating-point arithmetic.

---

## System Architecture

The accelerator is built as a streaming datapath with minimal control overhead.

### Processing stages

1. Serial reception of input bytes  
2. Assembly of sixteen-bit signed values  
3. Fixed bias offset adjustment  
4. Rectified activation gating  
5. Quantized eight-bit projection  
6. Serial transmission of outputs  

### Design characteristics

| Property | Implementation |
|---------|---------------|
| Arithmetic type | fixed-point signed |
| Compute style | fully streaming |
| Latency | one cycle per activation |
| Precision control | deterministic |
| Resource usage | minimal |
| Numerical drift | none |

---

## Hardware Components

- Serial receiver and transmitter  
- Input word buffer  
- Bias adjustment unit  
- Activation comparator and clamp  
- Quantization projection logic  
- Output serializer  

All neural operations are implemented using combinational and clocked logic.

---

## Validation Strategy

Correctness is established through end-to-end hardware/software co-verification.

### Validation flow

- Generate thousands of randomized sixteen-bit signed inputs  
- Transmit inputs to FPGA over serial link  
- Collect hardware-generated outputs  
- Compute reference outputs in software  
- Compare each value for exact agreement  

This method ensures physical hardware behavior matches the mathematical model precisely.

---

## Experimental Results

Testing was performed using five thousand randomized input values.

### Observed performance

| Metric | Measured Value |
|-------|---------------|
| Output correctness | 100 percent |
| Activation sparsity | approximately 63 percent |
| Data throughput | 11.25 kilobytes per second |
| Verification status | canonical pass |

### Result interpretation

- All outputs matched the software reference exactly  
- A majority of activations were suppressed by rectified gating, consistent with neural network statistics  
- Throughput was limited by serial communication bandwidth rather than compute speed  

These results confirm accurate quantized neural inference in real hardware.

---

## Platform Details

- FPGA device: Gowin Tang Nano 9K  
- Clock frequency: 27 megahertz  
- Communication interface: UART serial streaming  
- Arithmetic representation: fixed-point signed  

---

## Relevance to Neural Accelerator Design

This implementation reflects the core compute primitive used in:

- Tensor processing pipelines  
- Quantized inference engines  
- Edge AI hardware accelerators  

The project demonstrates:

- Low-precision neural arithmetic  
- Hardware-based activation nonlinearity  
- Streaming datapath execution  
- Formal golden-model verification  

It serves as a foundational block for scalable AI hardware architectures.

---

## Repository Structure

- Verilog accelerator implementation  
- Serial communication modules  
- Python verification and benchmarking harness  

---

## Potential Enhancements

- Parallel processing lanes  
- Vector and matrix computation units  
- On-chip activation memory  
- Sparsity-aware execution logic  
- High-bandwidth data interfaces  

---

## Summary

This repository delivers a rigorously validated neural compute accelerator implemented directly in FPGA logic.

It demonstrates deterministic fixed-point inference, professional verification practices, and real-time streaming execution, forming a strong foundation for advanced AI hardware systems.

