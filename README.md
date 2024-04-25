# InivitationGen
InivitationGen allows quick generation of boilerplate inivitation letters and statutory declarations.

# Build using the included `builder.py` script:
The following flags may be used when building the exe:
- `--no-selector` to skip version selector and automatically build using the next minor build number.
- `--deps` to install dependencies.

If no flags were used, no dependencies will be installed, and the builder will allow you to choose your own build version

# Usage
Input up to 3 guests' information, and up to 2 hosts' information. The input must contain at least 1 host and 1 guest. 

The `arrival` and `departure` dates for the guests are only available in the `Guest 1` tab, as the people included in the invitation must use the document to apply for their visa together.
Guest(s) arriving at different date needs to be included in a new invitation letter.

The `bearer` field are selectable only from `Host 1`, and is carried over to `Host 2`. It defaults to the hosts paying for their guests' expenses if nothing was selected.
The `attached` field is only available to `Host 1`, and is optional. If nothing was selected, the paragraph will be skipped entirely in the output letter.
