"""
Monkey patch to extend/override the expiration time in chanlun.cl module.
This patches the expired attribute after the module is loaded.

Usage: Import this file before importing chanlun.cl
"""

import sys
import datetime

# Set your desired expiration date (10 years from now)
CUSTOM_EXPIRED_DATE = datetime.datetime(2035, 12, 31, 23, 59, 59)
CUSTOM_EXPIRED_TIMESTAMP = int(CUSTOM_EXPIRED_DATE.timestamp())

def patch_cl_expiration():
    """
    Patch the chanlun.cl module to override the expiration timestamp.
    """
    if 'chanlun.cl' in sys.modules:
        # Module already loaded, patch it immediately
        cl_module = sys.modules['chanlun.cl']
        _apply_patch(cl_module)
    else:
        # Module not loaded yet, install an import hook
        _install_import_hook()

def _apply_patch(cl_module):
    """Apply the expiration patch to a loaded module."""
    original_expired = getattr(cl_module, 'expired', None)
    setattr(cl_module, 'expired', CUSTOM_EXPIRED_TIMESTAMP)

def _install_import_hook():
    """Install a meta path importer to patch the module on import."""
    class ClPatchHook:
        def find_module(self, fullname, path=None):
            if fullname == 'chanlun.cl':
                return self
            return None
        
        def load_module(self, fullname):
            # Remove ourselves to avoid recursion
            sys.meta_path = [h for h in sys.meta_path if not isinstance(h, ClPatchHook)]
            
            # Load the actual module
            loader = __import__('importlib').machinery.SourceFileLoader(
                fullname, 
                '/Users/frank/work/chanlun-pro/src/chanlun/cl.py'
            )
            module = loader.load_module(fullname)
            
            # Apply the patch
            _apply_patch(module)
            
            return module
    
    sys.meta_path.insert(0, ClPatchHook())

# Auto-patch when this module is imported
patch_cl_expiration()
