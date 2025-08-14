### Pre-Public Release TODO

**Before making repository public:**

1. **Email Verification** ✅
   - [ ] Verify `team@hoteval.com` email exists and is monitored
   - Used in: `python/pyproject.toml`, `python/hoteval/__init__.py`

2. **URL Verification** ✅
   - [ ] Confirm `dev.hoteval.com` dashboard URL is correct
   - [ ] Confirm `api.hoteval.com` backend URL is correct
   - [ ] Confirm `hoteval.com` main website is correct

3. **Final Steps** ⏳
   - [ ] Run full test suite: `make test-python`
   - [ ] Review all documentation for accuracy
   - [ ] Consider if git history should be cleaned before public release