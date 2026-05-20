import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time


def bytes_to_hex(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)


def hex_to_bytes(hex_text: str) -> bytes:
    cleaned = hex_text.replace("\n", " ").replace("\r", " ").replace(",", " ")
    return bytes.fromhex(cleaned)


class SerialCommandTool:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("HUNATE Serial")
        #self.root.iconbitmap("HUNATE.ico")
        self.root.geometry("760x520")

        self.port_var = tk.StringVar(value="COM9")
        self.baud_var = tk.StringVar(value="115200")
        self.timeout_var = tk.StringVar(value="1")
        self.wait_var = tk.StringVar(value="3")
        self.cmd_var = tk.StringVar(value="FA FF 20 00 00 19")

        self.make_ui()
        self.refresh_ports()

    def make_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frame)
        top.pack(fill=tk.X)

        ttk.Label(top, text="COM Port").grid(row=0, column=0, sticky=tk.W)
        self.port_combo = ttk.Combobox(top, textvariable=self.port_var, width=15)
        self.port_combo.grid(row=0, column=1, padx=5)

        ttk.Button(top, text="Refresh", command=self.refresh_ports).grid(row=0, column=2, padx=5)

        ttk.Label(top, text="Baudrate").grid(row=0, column=3, sticky=tk.W)
        ttk.Entry(top, textvariable=self.baud_var, width=10).grid(row=0, column=4, padx=5)

        ttk.Label(top, text="Timeout sec").grid(row=0, column=5, sticky=tk.W)
        ttk.Entry(top, textvariable=self.timeout_var, width=6).grid(row=0, column=6, padx=5)

        ttk.Label(frame, text="TX HEX Command").pack(anchor=tk.W, pady=(15, 0))
        ttk.Entry(frame, textvariable=self.cmd_var).pack(fill=tk.X)

        mid = ttk.Frame(frame)
        mid.pack(fill=tk.X, pady=10)

        ttk.Label(mid, text="Read wait sec").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(mid, textvariable=self.wait_var, width=6).grid(row=0, column=1, padx=5)

        ttk.Button(mid, text="Send Once", command=self.send_once).grid(row=0, column=2, padx=5)
        ttk.Button(mid, text="Clear Log", command=self.clear_log).grid(row=0, column=3, padx=5)

        ttk.Label(frame, text="Log").pack(anchor=tk.W)
        self.log = tk.Text(frame, height=22)
        self.log.pack(fill=tk.BOTH, expand=True)

    def refresh_ports(self) -> None:
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_combo["values"] = ports
        if ports and self.port_var.get() not in ports:
            self.port_var.set(ports[0])

    def append_log(self, text: str) -> None:
        self.log.insert(tk.END, text)
        self.log.see(tk.END)

    def clear_log(self) -> None:
        self.log.delete("1.0", tk.END)

    def send_once(self) -> None:
        try:
            port = self.port_var.get().strip()
            baudrate = int(self.baud_var.get().strip())
            timeout = float(self.timeout_var.get().strip())
            wait_sec = float(self.wait_var.get().strip())
            cmd = hex_to_bytes(self.cmd_var.get())

            self.append_log("\nTX HEX:\n")
            self.append_log(bytes_to_hex(cmd) + "\n")

            with serial.Serial(port=port, baudrate=baudrate, timeout=timeout) as ser:
                time.sleep(0.2)
                ser.reset_input_buffer()
                ser.reset_output_buffer()

                ser.write(cmd)
                ser.flush()

                time.sleep(wait_sec)

                data = ser.read_all()

            self.append_log("RX HEX:\n")
            if len(data) == 0:
                self.append_log("(no data)\n")
            else:
                self.append_log(bytes_to_hex(data) + "\n")

        except ValueError as exc:
            messagebox.showerror("Input Error", f"Input value error:\n{exc}")
        except serial.SerialException as exc:
            messagebox.showerror("Serial Error", f"Serial port error:\n{exc}")
        except Exception as exc:
            messagebox.showerror("Error", f"Unexpected error:\n{exc}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SerialCommandTool(root)
    root.mainloop()
