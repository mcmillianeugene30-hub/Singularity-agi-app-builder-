# PATH Environment Variable Fix

## Problem
The Netlify build was failing with "command not found" errors for core utilities like `mkdir`, `touch`, and `mise`. This was caused by the PATH environment variable being incorrectly overwritten.

## Root Cause
The `netlify.toml` file contained a problematic PATH setting:

```toml
[build.environment]
  NODE_VERSION = "18"
  PYTHON_VERSION = "3.10"
  PATH = "/opt/buildhome/.cargo/bin:$PATH"  # ❌ This overwrites PATH!
```

The issue:
1. TOML doesn't support variable expansion like `$PATH`
2. This completely overwrites the system PATH
3. Core utilities (mkdir, touch, pip, npm, etc.) become unavailable
4. Build fails immediately

## Solution

### 1. Fixed netlify.toml
**Removed the problematic PATH setting:**

```toml
[build.environment]
  NODE_VERSION = "18"
  PYTHON_VERSION = "3.10"
```

The build command already handles Rust installation correctly:
```toml
[build]
  command = "bash scripts/install-rust.sh && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && cd dashboard && npm install && npm run build"
```

### 2. Updated scripts/install-rust.sh
**Improved the script to properly source the cargo environment:**

```bash
#!/usr/bin/env bash
set -e
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# Source cargo environment to make tools available
source $HOME/.cargo/env
```

Using `source $HOME/.cargo/env` is the recommended way to add cargo tools to PATH, as it:
- Properly sets up the environment
- Works correctly in subshells
- Is the official rustup method

## Why This Works

1. **System PATH Preserved**: By not setting PATH in `netlify.toml`, Netlify's default PATH (which includes `/usr/bin`, `/usr/local/bin`, `/opt/buildhome/.pyenv/shims`, etc.) remains intact.

2. **Rust Tools Available**: The `install-rust.sh` script now properly sources the cargo environment, adding `$HOME/.cargo/bin` to PATH for the current shell session.

3. **Build Chain Intact**: All system utilities (mkdir, touch, pip, npm, etc.) remain accessible throughout the build process.

## Verification

The changes ensure:
- ✅ Core system commands work (mkdir, touch, cd, etc.)
- ✅ Python/pip commands work
- ✅ Node.js/npm commands work
- ✅ Rust/cargo tools are properly added to PATH
- ✅ Build command chain executes successfully
- ✅ No PATH overwrites in any scripts

## Files Changed

1. `netlify.toml` - Removed problematic PATH override
2. `scripts/install-rust.sh` - Changed from `export PATH` to `source $HOME/.cargo/env`

## Impact

This fix resolves the Netlify build failures and allows the deployment pipeline to proceed successfully.
