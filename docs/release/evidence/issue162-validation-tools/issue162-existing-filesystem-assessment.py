"""Read-only Darwin volume-capability inventory; not identity qualification."""
from pathlib import Path
import ctypes,os,json,datetime,tempfile
class AttrList(ctypes.Structure):
 _fields_=[('bitmapcount',ctypes.c_uint16),('reserved',ctypes.c_uint16),('commonattr',ctypes.c_uint32),('volattr',ctypes.c_uint32),('dirattr',ctypes.c_uint32),('fileattr',ctypes.c_uint32),('forkattr',ctypes.c_uint32)]
lib=ctypes.CDLL('libSystem.B.dylib',use_errno=True)
lib.getattrlist.argtypes=[ctypes.c_char_p,ctypes.POINTER(AttrList),ctypes.c_void_p,ctypes.c_size_t,ctypes.c_ulong]
lib.getattrlist.restype=ctypes.c_int
rows=[]
for label,path in [('workspace',str(Path.cwd())),('slash_tmp','/tmp'),('session_tmp',tempfile.gettempdir())]:
 request=AttrList(5,0,0,0x80020000,0,0,0);buf=(ctypes.c_uint32*9)()
 rc=lib.getattrlist(os.fsencode(path),ctypes.byref(request),buf,ctypes.sizeof(buf),0)
 row={'authorized_root':label,'path':path,'query':'getattrlist ATTR_VOL_INFO | ATTR_VOL_CAPABILITIES (read-only)','return':rc}
 if rc:
  row['errno']=ctypes.get_errno()
 else:
  assert buf[0]>=36
  row.update({'case_sensitive_flag_valid':bool(buf[5]&0x100),'case_sensitive_volume_flag':bool(buf[1]&0x100),'buffer_bytes':buf[0]})
 rows.append(row)
result={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authorized_roots':rows,
 'safe_existing_authorized_compatible_filesystem_identified':False,
 'limits':'Volume flags are metadata, not finite-witness qualification or proof about every directory. Existing actual Mac witness tests establish alias refusal in their measured contexts. No same-device or private-child equivalence is used to grant permission.',
 'other_mounts':'Read-only inventory found additional local mounts outside authorized writable roots, read-only system/provider mounts, and a network filesystem. None was adopted, written, or qualified.',
 'diskutil_status':'Read-only diskutil info queries could not use DiskManagement framework; mount inventory and direct read-only getattrlist used instead.',
 'actions':{'filesystem_created_mounted_reformatted':False,'permissions_changed':False,'computer_switched':False,'outside_scope_scratch_created':False,'new_native_qualification_claimed':False},
 'source':'Installed Apple SDK sys/attr.h: ATTR_VOL_CAPABILITIES 0x00020000, ATTR_VOL_INFO 0x80000000, VOL_CAP_FMT_CASE_SENSITIVE 0x00000100'}
Path('../validation/issue162-existing-filesystem-assessment.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'authorized_root_capabilities':[{'root':r['authorized_root'],'valid':r.get('case_sensitive_flag_valid'),'case_sensitive':r.get('case_sensitive_volume_flag'),'error':r.get('errno')} for r in rows],'safe_authorized_compatible_context_identified':False},indent=2))
