# cucm_appuser_device_assoc_sql
This simple script will create SQL command that can be run in the CLI (SSH session) of a Cisco Call Manager (CUCM) to associate (or disassoicate)
devices from an Application user (Or list of multiple application users)  
The script inputs a text file with a list of devices to be assoicated (or disassociated)  
One device per row.  
It will output 2 files per Application user provided  
One to associate, one to disassoicate  

### Example devices.txt file is provided  
rename `devices.txt.example` to `devices.txt`

### Example Associate output
`run sql insert into applicationuserdevicemap (fkapplicationuser, fkdevice, tkuserassociation) select au.pkid, d.pkid, 1 from applicationuser au cross join device d where au.name = 'DAL_RMCM' and d.name in ('SEP_ap231','csf_mylogin1','CIPCUCCXADMIN','SEP00152B176C99') and d.pkid not in (select fkdevice from applicationuserdevicemap where fkapplicationuser = au.pkid)`  

`run sql insert into applicationuserdevicemap (fkapplicationuser, fkdevice, tkuserassociation) select au.pkid, d.pkid, 1 from applicationuser au cross join device d where au.name = 'WFM_REC01' and d.name in ('SEP_ap231','csf_mylogin1','CIPCUCCXADMIN','SEP00152B176C99') and d.pkid not in (select fkdevice from applicationuserdevicemap where fkapplicationuser = au.pkid)`  

### Example Disassociate output

`run sql delete from applicationuserdevicemap where fkapplicationuser = (select pkid from applicationuser au where au.name = 'DAL_RMCM') and fkdevice in (select pkid from device d where d.name in ('SEP_ap231','csf_mylogin1','CIPCUCCXADMIN','SEP00152B176C99'))`  

`run sql delete from applicationuserdevicemap where fkapplicationuser = (select pkid from applicationuser au where au.name = 'WFM_REC01') and fkdevice in (select pkid from device d where d.name in ('SEP_ap231','csf_mylogin1','CIPCUCCXADMIN','SEP00152B176C99'))`  

