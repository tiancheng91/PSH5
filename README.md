# PS5 Relapse Exploit
Supported firmware: 7.00 through 13.60.

## Usage
- In the network settings, set Primary DNS to `45.56.67.85` (Recommended)
- Run `python serve.py` locally, or open https://ntfargo.github.io/Relapse-Exploit/ on the PS5.
- The default payloads are stored in `payloads/` after a successful run, the ELF loader listens on port `9021`.
- Minimal default autoload keeps only OnionHEN (homebrew and FTP on TCP `1337`) and Payload Manager (manual payload loading). The WebKit Autoloader installer runs last.
- Optional modules and emulator installation calls are commented out in `src/kexp.js`, in their original order. To enable a module, uncomment its save/install calls and its `AUTOLOAD_NAMES` entry where applicable. Existing optional files are kept, but excluded from the rebuilt autoload list.
- The Python server listens only on `127.0.0.1:8000`, so other devices cannot connect directly. `local_ip()` can detect a `192.168.*` address on Linux and falls back to loopback; it does not change the listener.
- Leave the Autoloader page open until installation finishes, then reboot and open **WebKit Autoloader**.

## Stability notes
Webkit may need several attempts, reload the page if the browser stalls. The kernel exploit may hang or panic the console, so reboot before trying again if that happens.

## Exploit chain
Browser stage uses JSC info leaks and a structured clone object pool mismatch to corrupt a typedarray. The kernel stage combines a address leak with an `aio_multi_wait` uaf race to establish kernel r/w.

## Credits
ntfargo, ufm42, Sonic-Iso, Jordy, Dr. Yenyen, TheFlow, SlidyBat,  Flatz, cow, nhk, bollarz, Sleirsgoevy, EchoStretch, EarthOnion.

## Disclaimer
This project is intended for **educational and security research purposes only**. It does not endorse piracy, unauthorized access, or misuse of commercial devices. Use it only on devices you own or are authorized to test, and comply with applicable laws and regulations.

The software is provided as-is, without warranty. You assume the risks of using it, including system instability, data loss, and account bans. The maintainers accept no liability for resulting damage. 
