#  Hex Serial Monitor Tool for Embedded UART Debugging

## Overview

This project is a simple serial monitoring tool for embedded UART debugging.

It was created because general serial terminal programs such as Tera Term display received data as ASCII text.  
When the received UART data contains binary or hexadecimal values, the output may appear broken, unreadable, or garbled.

This tool is intended to display received UART data in hexadecimal format so that raw packets can be checked clearly.

## Purpose

The main purpose of this tool is to check raw UART communication data from embedded devices.

It is useful when debugging:

- MCU UART communication
- Sensor response packets
- Custom serial protocols

## Why This Tool Is Needed

Tera Term is useful for normal text-based UART logs.

However, when the MCU sends binary data such as:

```text
0x5A 0xA5 0x07 0x82 0x00 0x84
<img width="758" height="523" alt="image" src="https://github.com/user-attachments/assets/92fe2194-9213-4271-b578-b0bfbbc1e301" />
