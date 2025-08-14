### Pre-Public Release TODO

**Before making repository public:**

1. **Email Verification** ✅
   - [ ] Verify `team@hoteval.com` email exists and is monitored
   - Used in: `python/pyproject.toml`, `python/hoteval/__init__.py`

2. **URL Verification** ✅
   - [ ] Confirm `dev.hoteval.com` dashboard URL is correct
   - [ ] Confirm `api.hoteval.com` backend URL is correct
   - [ ] Confirm `hoteval.com` main website is correct

3. **PyPI Registration & Publishing** 🚀
   - [ ] Complete PyPI account registration and setup
   - [ ] Configure trusted publishing for GitHub Actions
   - [ ] Verify `hoteval` package name is available on PyPI
   - [ ] Publish v0.0.9000 to PyPI (built package ready in release)
   - [ ] Test installation: `pip install hoteval==0.0.9000`

4. **Final Steps** ⏳
   - [ ] Run full test suite: `make test-python`
   - [ ] Review all documentation for accuracy
   - [ ] Consider if git history should be cleaned before public release