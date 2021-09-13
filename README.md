# Workshop Flow Converter

## It is a part of the [Image Processing Workshop](https://github.com/ekarpovs/image-processing-workshop) project. The converter converts a user friendly flow description (worksheet) into finite state machine definition

### File system structure

    Anywhere in a file system:
_____
    |__ /data/ __ files for processing
    |
    

    |__ /flow_converter/ The project files
    |

## Local Installation

```bash
cd flow_converter
pip install -e .
```

## Usage

```bash
python run.py -m <worksheet full name> -f <output path>
```
