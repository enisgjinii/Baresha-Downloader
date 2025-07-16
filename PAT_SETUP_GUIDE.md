# Personal Access Token Setup Guide

## 🔐 **Your PAT Token**
```
<YOUR_PAT_TOKEN_HERE>
```

## 📋 **Step-by-Step Setup**

### Step 1: Add PAT to Repository Secrets

1. **Go to your repository**: https://github.com/enisgjinii/Baresha-Downloader
2. **Navigate to**: Settings → Secrets and variables → Actions
3. **Click**: "New repository secret"
4. **Fill in**:
   - **Name**: `PAT_TOKEN`
   - **Value**: `<YOUR_PAT_TOKEN_HERE>`
5. **Click**: "Add secret"

### Step 2: Verify Workflow Configuration

The workflows have been updated to use the PAT token:

- **`.github/workflows/auto-release.yml`**: Uses `${{ secrets.PAT_TOKEN }}`
- **`.github/workflows/release.yml`**: Uses `${{ secrets.PAT_TOKEN }}`

### Step 3: Test the Setup

You can test the setup in several ways:

#### Option A: Create a Conventional Commit
```bash
git commit -m "feat: test PAT token setup"
git push origin master
```

#### Option B: Create a Manual Tag
```bash
python create_tag.py 0.1.1 "Test release with PAT"
```

#### Option C: Use the Helper Script
```bash
python create_tag.py patch "Bug fix test"
```

## 🔍 **Verification Steps**

1. **Check GitHub Actions Tab**: Should show workflows running successfully
2. **Check Releases Page**: Should show new releases being created
3. **Check Tags Page**: Should show new tags being pushed

## 🛠️ **Troubleshooting**

### If PAT doesn't work:

1. **Check Token Permissions**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Ensure the token has `repo` and `workflow` scopes

2. **Check Repository Settings**:
   - Go to Settings → Actions → General
   - Ensure "Allow GitHub Actions to create and approve pull requests" is enabled

3. **Check Workflow Permissions**:
   - Go to Settings → Actions → General → Workflow permissions
   - Set to "Read and write permissions"

### If you need to regenerate the token:

1. **Go to**: GitHub → Settings → Developer settings → Personal access tokens
2. **Click**: "Generate new token (classic)"
3. **Select scopes**: `repo`, `workflow`
4. **Copy the new token** and update the repository secret

## 🔒 **Security Notes**

- **Keep your PAT secure** - Don't share it publicly
- **Use repository secrets** - Never hardcode tokens in workflows
- **Rotate tokens regularly** - Consider regenerating every 90 days
- **Limit token scope** - Only grant necessary permissions

## 📝 **What's Been Configured**

✅ **Workflow files updated** to use PAT token
✅ **Git credential helper** configured for local use
✅ **Repository secrets** ready to be added
✅ **Permission fixes** applied to workflows

## 🚀 **Next Steps**

1. **Add the PAT to repository secrets** (Step 1 above)
2. **Test with a conventional commit** or manual tag
3. **Monitor GitHub Actions** for successful execution
4. **Check releases page** for new releases

The PAT token setup should resolve all permission issues with GitHub Actions tag creation and releases! 