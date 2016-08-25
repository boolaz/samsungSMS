# samsungSMS

If you try to extract the content from some Samsung mobile phones (B550H and some other types as well) with Cellebrite UFED, you won't be able to dump the list of the SMS sent and received from the device. If you try to do it with MSAB XRY, you'll be presented with a bunch of .VMG files that might be very numerous (one for each SMS). Therefore, presenting them in your report might be a tough task to achieve.

The purpose of this tool is to convert all the .VMG files resulting from an XRY extraction to a neat CSV file that you can use to build your report in a simple way.

Of course, this script I release today is related to Samsung phones and can be adapted to various types of mobile phones.

## Prerequisites

samsungSMS has been developed in python 2.7 and has been successfully tested on Linux Ubuntu 14.04 LTS, MacOSX 10.11.6 El Capitan and Windows 8.1 x64. This tool doesn't require any additional python modules to be run.
A stand-alone binary version for windows is also available for download.

## Syntax

Simply execute the python script or the windows binary with the directory containing the .VMG SMS files as an argument

    $ ./samsungSMS.py SMS_directory

As an output, you'll get a text CSV file with the details of all the SMS files


Stay tuned for updates and please, feel free to report any bug to the author.
