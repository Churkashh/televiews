# TeleViews

## Overview 🚀
**TeleViews** is a powerful, high-speed tool designed to boost view counts on posts in Telegram channels. It supports multithreading for efficient processing and provides clear, error-handled execution with detailed log output. Whether you're handling single or bulk operations, TeleViews ensures smooth performance.

---

### ✨ Features
- **Multithreading Support**: Processes multiple view-boosting tasks simultaneously for maximum efficiency.
- **Flexible Configuration**: Easily adjust thread count and logging preferences in the configuration file.
- **Detailed Console Logs**: Clear and concise logs to monitor view-boosting operations.
- **Proxy Error Logging**: Option to toggle proxy error logging for cleaner output.

---

### ⚙️ Setup & Usage

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. **Configure proxies**:
   - TeleViews requires proxies. Add your proxies in the `proxies.txt` file in the format `user:pass@host:port`. Example:
     ```
     user1:pass1@127.0.0.1:8080
     user2:pass2@127.0.0.1:8080
     ```

3. Configure settings in `config.yaml`:
    ```yaml
    main:
      threads: 10
      log_proxy_err: false
      proxy_per_view: false
      remove_proxies: false
      detailed_exception_log: false
    ```

   - **threads**: Number of threads to run.
   - **log_proxy_err**: Set to `true` to log proxy-related errors (default: `false`).
   - **proxy_per_view**: Set to `true` to use one proxy per view (default: `false`).
   - **remove_proxies**: Set to `true` to remove used proxies from the `proxies.txt` if proxy_per_view set to `true` (default: `false`).
   - **detailed_exception_log**: Set to `true` for detailed exception logs (default: `false`).

4. Run the tool:
    ```bash
    python main.py
    ```

---

### 🔧 Configuration
Modify `config.yaml` to adjust settings as needed:
```yaml
main:
  threads: 10
  log_proxy_err: false
  proxy_per_view: false
  remove_proxies: false
  detailed_exception_log: false
```

---

### 📜 License
This project is distributed under the MIT license. See the [LICENSE](LICENSE) file for details. Use of this software is permitted for educational purposes only. All actions using this tool must be performed within the framework of the law. The owner is not responsible for the use of this software.
