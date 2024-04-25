# InivitationGen
InivitationGen allows quick generation of boilerplate inivitation letters and statutory declarations.

# Usage
- download the latest build.
- unzip the contents.
- run the executable.

# Build using the included `builder.py` script:
## flags:
- no flags will build the exe with the next minor build number.
- `--no-selector` to skip version selector and automatically build using the next minor build number.
- `--deps` to install dependencies.

# Usage
Input up to 3 guests' information, and up to 2 hosts' information. The input must contain at least 1 host and 1 guest. 

The `arrival` and `departure` dates for the guests are only available in the `Guest 1` tab, as the people included in the invitation must use the document to apply for their visa together.
Guest(s) arriving at different date needs to be included in a new invitation letter.

The `bearer` field are selectable only from `Host 1`, and is carried over to `Host 2`. It defaults to the hosts paying for their guests' expenses if nothing was selected.
The `attached` field is only available to `Host 1`, and is optional. If nothing was selected, the paragraph will be skipped entirely in the output letter.
