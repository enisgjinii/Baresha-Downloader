# GitHub Actions Permission Fix Guide

## Problem
You're encountering this error when GitHub Actions tries to create tags:
```
remote: Permission to enisgjinii/Baresha-Downloader.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/enisgjinii/Baresha-Downloader/': The requested URL returned error: 403
Error: Process completed with exit code 128.
```

## Root Cause
The `GITHUB_TOKEN` used by GitHub Actions doesn't have sufficient permissions to push tags to the repository by default.

## Solutions

### Solution 1: Use Repository Permissions (Recommended)

I've already updated your workflow files to include the necessary permissions. The changes include:

1. **Added job-level permissions** in `.github/workflows/auto-release.yml`:
   ```yaml
   permissions:
     contents: write
     issues: write
     pull-requests: write
   ```

2. **Added job-level permissions** in `.github/workflows/release.yml`:
   ```yaml
   permissions:
     contents: write
   ```

### Solution 2: Use Personal Access Token (Alternative)

If the repository permissions don't work, you can use a Personal Access Token:

1. **Create a Personal Access Token**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `workflow`
   - Copy the token

2. **Add the token to repository secrets**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PAT_TOKEN`
   - Value: Your personal access token

3. **Update the workflow** to use the PAT:
   ```yaml
   env:
     GITHUB_TOKEN: ${{ secrets.PAT_TOKEN }}
   ```

### Solution 3: Manual Tag Creation (Fallback)

If GitHub Actions continues to fail, you can create tags manually:

1. **Use the provided script**:
   ```bash
   python create_tag.py 0.1.0 "Initial release"
   ```

2. **Or create tags manually**:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

## Testing the Fix

1. **Commit and push the workflow changes**:
   ```bash
   git add .github/workflows/
   git commit -m "fix: add proper permissions to GitHub Actions workflows"
   git push origin main
   ```

2. **Test with a conventional commit**:
   ```bash
   git commit -m "feat: test auto-release workflow"
   git push origin main
   ```

3. **Or create a tag manually**:
   ```bash
   python create_tag.py 0.1.0
   ```

## Verification

After pushing changes, check:

1. **GitHub Actions tab** - Should show the workflow running
2. **Releases page** - Should show the new release
3. **Tags page** - Should show the new tag

## Troubleshooting

### If permissions still don't work:

1. **Check repository settings**:
   - Go to Settings → Actions → General
   - Ensure "Allow GitHub Actions to create and approve pull requests" is enabled

2. **Check workflow permissions**:
   - Go to Settings → Actions → General → Workflow permissions
   - Set to "Read and write permissions"

3. **Use PAT token** as described in Solution 2

### If manual tag creation fails:

1. **Check git credentials**:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **Check remote URL**:
   ```bash
   git remote -v
   ```

3. **Authenticate with GitHub**:
   ```bash
   git push origin v0.1.0
   # Enter your GitHub credentials when prompted
   ```

## Files Modified

- `.github/workflows/auto-release.yml` - Added permissions and proper token usage
- `.github/workflows/release.yml` - Added permissions
- `create_tag.py` - Helper script for manual tag creation
- `GITHUB_ACTIONS_FIX.md` - This guide

## Next Steps

1. Commit and push the workflow changes
2. Test with a conventional commit or manual tag
3. Monitor the GitHub Actions tab for successful execution
4. Check the Releases page for the new release

The fixes should resolve the permission issues and allow your GitHub Actions workflows to create tags and releases successfully. 