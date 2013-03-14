#!/usr/bin/python
'''
mpsh_flashfds.py
monitor libflashplayer file descriptors and update mpsh flash fd browser every n seconds
'''

import subprocess, os, sys, time, signal
sys.path.append('%s/apps/mpsh' %os.environ['HOME'])
from mpsh import MPlayer
from mpsh_os_extensions import pgrep

flashfds_path = '%s/.mplayer/flashfds' %os.environ['HOME']

def on_exit(sig, func=None):
    print 'got signal: %s' % sig
    rm_symlinks()
    mp.menu('cancel')
    sys.exit(0)

def rm_symlinks(path=flashfds_path):
    for symlink in os.listdir(path):
        os.remove(os.path.join(path,symlink))

def checkrunning(regexp="/usr/bin/python.*flashfds.py"):
    pids = pgrep( regexp)
    mypid = str( os.getpid() )
    myppid = str( os.getppid() )
    if mypid in pids:
        pids.remove( mypid )
    if myppid in pids:
        pids.remove( myppid )

    if pids:
        print 'found other instance(s) running:',
        for pid in pids:
            if not pid == str(os.getpid()): 
	        print pid
        print '\n',
        sys.exit(1)

if __name__=='__main__':
    ''' main '''
    checkrunning()
    
    for sig in [ signal.SIGINT, 
		         signal.SIGHUP, 
		         signal.SIGTERM ]:
        signal.signal(sig, on_exit)
    
    iterations = 0 # 0 == unlimited
    flashlines = []
    lastD = {}
    
    mp = MPlayer()
    #mp.populate_cmdlist()

    sys.stdout.write("\x1b[2J") # clear screen
    sys.stdout.write("\x1b[0;0H") # cursor posistion 0,0

    while iterations == 0:
        pids = pgrep( 'lib.*flashplayer', greedy=True )
        #more_pids = pgrep( 'rtmpdump', greedy=True )
        
       # pids.extend( more_pids )
        if not pids:
            print 'No flashplayer instance(s) found. Sleep 10s'
            time.sleep(10)
            continue
        
        sys.stdout.write("\x1b[1;0H")
        print "{0:10} {1:6} {2:4} {3:10} {4:10} {5:25} \t {6:20}".format( "name", "pid", "fd", "size", "inode", "path", "fdpath" )
        sys.stdout.write("\x1B[J") # clear from cursor down
	
        keepD = {}
  
        for pid in pids:
            lsof = subprocess.Popen(['lsof', '-p', pid], stdout=subprocess.PIPE, stderr=open('/dev/null','w'),close_fds=True)
            lsof.wait()      
            flashlines = [ line.split() for line in lsof.stdout.readlines() for q in [ 'tmp/Flash', ':1935' ] if q in line ]

            for ln in flashlines:
                fd = ln[3][:-1]
                inode = ln[7]
                filename = ln[8].rsplit('/')[-1]
                keepD[ inode ] = [ pid, fd, filename ]
                print "{1:10} {2:6} {0:4} {7:10} {8:10} {9} \t file:///proc/{2}/fd/{0}".format(fd, *ln)
        
        if keepD != lastD:   
            rm_symlinks()

            for i in keepD.keys():
                pid, fd, fn = keepD.get(i)
                symlink = os.path.join( flashfds_path, '%s_%s_fd_%s' %(fn, pid, fd))

                if not os.path.islink( symlink ):
                    os.symlink( '/proc/%s/fd/%s' %(pid,fd), symlink )

                    if not i in lastD.keys():
                        instance = MPlayer( symlink )
                        

        lastD = keepD.copy()
        time.sleep (3)

#	    if mp._mpsh_mplayer_in:
 #    		mp._mpsh_mplayer_in.write('menu cancel\n')
	#    	mp._mpsh_mplayer_in.write('set_menu open_flash_fd\n')
        
mp._clean_up()
exit(0)

