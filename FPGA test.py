import serial
import time
import numpy as np

def main():
    # --- CONFIGURATION ---
    PORT = 'COM6'  # Update this for your specific system
    BAUD = 115200
    BIAS = -25
    TEST_SIZE = 5000  # Number of 16-bit weights to process
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=2.0)
        ser.reset_input_buffer()
        print(f"📡 Serial link active on {PORT}. Initializing NPU test...")

        # 1. Generate 16-bit signed weights (Little Endian)
        tx_weights = np.random.randint(-1000, 1000, size=TEST_SIZE, dtype=np.int16)
        tx_bytes = tx_weights.tobytes()

        # 2. Transmit to FPGA
        print(f"🚀 Streaming {len(tx_bytes)} bytes...")
        start_time = time.time()
        ser.write(tx_bytes)

        # 3. Collect 8-bit processed results
        rx_data = b''
        while len(rx_data) < TEST_SIZE and (time.time() - start_time) < 5:
            if ser.in_waiting:
                rx_data += ser.read(ser.in_waiting)
        
        total_time = time.time() - start_time
        ser.close()

        # 4. Canonical Validation (Software Golden Model)
        actual = np.frombuffer(rx_data, dtype=np.uint8)
        expected = np.array([
            (0 if (int(w) + BIAS) < 0 else (int(w) >> 8) & 0xFF) 
            for w in tx_weights
        ], dtype=np.uint8)

        # 5. Final Metrics Report
        accuracy = (np.sum(actual == expected[:len(actual)]) / TEST_SIZE) * 100
        throughput = (len(tx_bytes) / 1024) / total_time

        print("\n" + "="*40)
        print(f"🏆 NPU VALIDATION COMPLETE")
        print(f"Accuracy   : {accuracy:.2f}%")
        print(f"Sparsity   : {(np.sum(actual == 0)/TEST_SIZE)*100:.2f}%")
        print(f"Throughput : {throughput:.2f} KB/s")
        print(f"Result     : {'✅ CANONICAL PASS' if accuracy == 100 else '❌ MATH ERROR'}")
        print("="*40)

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()