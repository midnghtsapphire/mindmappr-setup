# GitHub Pages Deployment Guide for MIDNGHTSAPPHIRE

## Live Websites Hosted on GitHub Pages

### Identified Domains
1. meetaudreyevans.com
2. yumyumcode.com
3. growlingeyes.com
4. truthslayer.com
5. glowstarlabs.com
6. audreyevansofficial.com (pending)
7. reesereviews.com

## Deployment Steps

### 1. Repository Setup
- Create/Verify repositories for each domain
- Ensure repositories are configured for GitHub Pages
- Use `gh-pages` branch or `docs/` folder for static site hosting

### 2. Continuous Deployment Workflow
- Implement GitHub Actions for automatic deployment
- Validate build process for each site
- Set up automatic SSL certificate generation
- Configure custom domain settings

### 3. Accessibility Considerations
- Implement WCAG AAA compliance
- No blue-light mode
- Screen reader-friendly
- Alt text for all media
- Neurodivergent-friendly design

### 4. Performance Optimization
- Minimize asset sizes
- Implement lazy loading
- Use GitHub Pages CDN
- Optimize for mobile and assistive technologies

### 5. Monitoring and Maintenance
- Set up uptime monitoring
- Automated accessibility checks
- Regular security scans
- Performance auditing

## Recommended GitHub Pages Configuration
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Pages
        uses: actions/configure-pages@v3
      - name: Build with Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: ./
          destination: ./_site
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

## Accessibility Checklist
- [ ] Semantic HTML
- [ ] Keyboard navigation
- [ ] Color contrast
- [ ] Alt text for images
- [ ] ARIA labels
- [ ] No autoplay media
- [ ] Responsive design
- [ ] Text resizing support

---

*Last Updated:* 2026-02-18