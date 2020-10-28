# cucm_appuser_device_assoc_sql
This simple script will create SQL command that can be run in the CLI (SSH session) of a Cisco Call Manager (CUCM) to associate (or disassoicate)
devices from an Application user (Or list of multiple application users)  
The script inputs a text file with a list of devices to be assoicated (or disassociated)  
One device per row.  
It will output 2 files per Application user provided  
One to associate, one to disassoicate  
