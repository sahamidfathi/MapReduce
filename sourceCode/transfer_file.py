import sys
import paramiko
import glob

class SSHConnection(object):
    
	def __init__(self, host, username, password, port=22):
		"""Initialize and setup connection"""
		self.sftp = None
		self.sftp_open = False
        
		# open SSH Transport stream
		self.transport = paramiko.Transport((host, port))
        
		self.transport.connect(username=username, password=password)
        
    
	def _openSFTPConnection(self):
		"""
		Opens an SFTP connection if not already open
		"""
		if not self.sftp_open:
			self.sftp = paramiko.SFTPClient.from_transport(self.transport)
			self.sftp_open = True
   

	def get(self, remote_path, local_path=None):
		"""
		Copies a file from the remote host to the local host.
		"""
		self._openSFTPConnection()        
		self.sftp.get(remote_path, local_path)        
            
    
	def put(self, local_path, remote_path=None):
		"""
		Copies a file from the local host to the remote host
		"""
		self._openSFTPConnection()
		self.sftp.put(local_path, remote_path)
        
    
	def close(self):
		"""
		Close SFTP connection and ssh connection
		"""
		if self.sftp_open:
			self.sftp.close()
			self.sftp_open = False
		self.transport.close()
        
if __name__ == "__main__":
	host = sys.argv[3] #"cs4459-vm1.gaul.csd.uwo.ca" #
	username = sys.argv[4] #"sfathi4" #
	pw = sys.argv[5] #"**"#
 
	origin = glob.glob('./inputFile/*part' + sys.argv[2] + '*')[0]
	dst = '/home/' + username + '/Documents/' + sys.argv[1] + '_part' + sys.argv[2] + '.txt'
    
	ssh = SSHConnection(host, username, pw)
	ssh.put(origin, dst)
	ssh.close()
    
