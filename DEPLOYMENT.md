# Deployment Guide for Streamlit Cloud

This guide explains how to deploy the Workflow Automator to Streamlit Cloud with proper browser support.

## Prerequisites

1. A GitHub repository with your code
2. A Streamlit Cloud account
3. OpenAI API key configured

## Files Required for Deployment

The following files are essential for successful deployment:

### Core Files
- `main.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies for Playwright
- `.streamlit/config.toml` - Streamlit configuration

### Browser Setup Files
- `setup_browsers.py` - Browser installation script
- `browser_setup.py` - Browser environment configuration
- `config.py` - Application configuration
- `browser.py` - Browser automation logic

## Deployment Steps

### 1. Prepare Your Repository

Ensure all files are committed to your GitHub repository:

```bash
git add .
git commit -m "Add browser setup for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set the main file path to: `main.py`
4. Add your environment variables:
   - `OPENAI_API_KEY` - Your OpenAI API key

### 3. Environment Variables

Set these environment variables in Streamlit Cloud:

```
OPENAI_API_KEY=your_openai_api_key_here
DEBUG_MODE=False
LOG_LEVEL=INFO
```

## Browser Installation Process

The application automatically handles browser installation on startup:

1. **Environment Setup**: Sets proper paths for Linux cloud deployment
2. **Browser Installation**: Installs Playwright Chromium browser
3. **Verification**: Tests browser functionality
4. **Error Handling**: Graceful fallback if installation fails

## Troubleshooting

### Common Issues

#### 1. Browser Installation Fails

**Error**: `FileNotFoundError: No such file or directory: '/home/appuser/.cache/ms-playwright/chromium-1181/chrome-linux/chrome'`

**Solution**: 
- Ensure `packages.txt` is present with all system dependencies
- Check that `setup_browsers.py` is being executed
- Verify environment variables are set correctly

#### 2. Memory Issues

**Error**: Browser crashes or runs out of memory

**Solution**:
- The browser profile is configured with memory-optimized settings
- Uses single-process mode for cloud deployment
- Disables unnecessary features to reduce memory usage

#### 3. Timeout Issues

**Error**: Browser operations timeout

**Solution**:
- Browser is configured with optimized timeouts
- Uses headless mode for better performance
- Implements retry logic for failed operations

### Debug Mode

To enable debug mode, set the environment variable:

```
DEBUG_MODE=True
```

This will provide more detailed logging for troubleshooting.

## Performance Optimization

The deployment is optimized for Streamlit Cloud:

1. **Browser Profile**: Configured with cloud-optimized settings
2. **Memory Usage**: Minimized through single-process mode
3. **Startup Time**: Reduced through efficient browser installation
4. **Error Recovery**: Graceful handling of browser failures

## Monitoring

Monitor your deployment through:

1. **Streamlit Cloud Dashboard**: Check deployment status and logs
2. **Application Logs**: View browser setup and execution logs
3. **Error Tracking**: Monitor for browser-related errors

## Support

If you encounter issues:

1. Check the Streamlit Cloud logs for error messages
2. Verify all required files are present in your repository
3. Ensure environment variables are correctly set
4. Test browser functionality locally before deploying

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Install system dependencies (macOS)
brew install wget gnupg ca-certificates

# Run browser setup
python setup_browsers.py

# Run the application
streamlit run main.py
```

This ensures your local environment matches the cloud deployment configuration. 