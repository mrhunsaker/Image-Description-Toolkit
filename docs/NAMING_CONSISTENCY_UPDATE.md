# File Naming Consistency Update

## Overview
Updated all file names to follow consistent naming patterns for better organization and clarity.

## Naming Pattern Established

### README Files
**Pattern**: `{script_name}_README.md`

| Old Name | New Name | Script |
|----------|----------|---------|
| `VideoREADME.md` | `video_frame_extractor_README.md` | `video_frame_extractor.py` |
| `CONVERT_README.md` | `ConvertImage_README.md` | `ConvertImage.py` |
| `HTML_README.md` | `descriptions_to_html_README.md` | `descriptions_to_html.py` |
| *(created new)* | `image_describer_README.md` | `image_describer.py` |
| *(unchanged)* | `WORKFLOW_README.md` | `workflow.py` |
| *(unchanged)* | `README.md` | Project root overview |

### Configuration Files
**Pattern**: `{script_name}_config.json`

| Old Name | New Name | Script |
|----------|----------|---------|
| `config.json` | `image_describer_config.json` | `image_describer.py` |
| `frame_extractor_config.json` | `video_frame_extractor_config.json` | `video_frame_extractor.py` |
| *(unchanged)* | `workflow_config.json` | `workflow.py` |
| *(unchanged)* | `requirements.txt` | All dependencies consolidated |

## Files Updated

### Scripts Updated
- `image_describer.py` - Updated all config file references
- `video_frame_extractor.py` - Updated config file references
- `workflow.py` - Updated config file references in workflow step
- `workflow_config.json` - Updated referenced config file names
- All scripts now use the organized workflow output structure by default

### Documentation Updated
- `README.md` - Updated all file references, help text, and workflow usage
- `WORKFLOW_README.md` - Updated config file references and workflow steps
- `CONFIGURATION.md` - Updated all config file references and options
- `IMPLEMENTATION_SUMMARY.md` - Updated config file references and output structure
- `TESTING_GUIDE.md` and `TESTING_README.md` - Updated for new test suite and structure
- All script-specific READMEs updated for CLI options and output conventions

### New Documentation Created
- `image_describer_README.md` - Comprehensive documentation for image_describer.py
- `video_frame_extractor_README.md` - Comprehensive documentation for video_frame_extractor.py
- `ConvertImage_README.md` - Comprehensive documentation for ConvertImage.py
- `descriptions_to_html_README.md` - Comprehensive documentation for descriptions_to_html.py

## Benefits of Consistent Naming

1. **Clear Association**: Each script has an obviously related README and config file
2. **Easy Discovery**: Users can quickly find documentation for any script
3. **Scalable Pattern**: Easy to follow when adding new scripts
4. **Reduced Confusion**: No ambiguous file names like "config.json" or "HTML_README.md"
5. **Better Organization**: Logical grouping of related files

## Verification

All scripts tested and working correctly with new config file names and output structure:
- \u2705 `image_describer.py --help` shows correct config file references and output directory
- \u2705 `video_frame_extractor.py` references correct config file and output directory
- \u2705 `workflow.py` uses updated config file names and organizes outputs in workflow_output/
- \u2705 All documentation updated consistently
- \u2705 All requirements consolidated in a single requirements.txt

## Migration Notes

For users with existing configurations:
- Rename `config.json` to `image_describer_config.json`
- Rename `frame_extractor_config.json` to `video_frame_extractor_config.json`
- All content and structure of config files remains unchanged - only filenames changed
- Remove any `--no-workflow` flags from your scripts; all outputs are now organized automatically

The system will create default config files with new names if old ones are not found, ensuring smooth transition.
