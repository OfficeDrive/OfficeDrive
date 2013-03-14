#!/usr/bin/python
#
# mpsh.py
#

__mpsh_version__ = '1.0'

import os, sys
import select
import subprocess
import time
import signal
import random

from weakref import WeakValueDictionary
from mpsh_os_extensions import *

os.environ['TERM'] = 'linux'
os.environ['MPLAYER_CHARSET'] = 'utf8'

class MPlayer(object):
    ''' 
    mplayer interface and interactive shell

    p.loadfile('/desktop/youtubevid.flv')
    p.pause()
    p.quit()

	mpsh features: 
        - interactive mplayer shell
        - filename, commmand, object and attribute completion
        - mplayer documentation
        - subtitle downloads from opensubtitles.org
        - watch and save flash streams
	'''
    instances = WeakValueDictionary()

    mplayer_binary = '%s/%s' %( os.environ['HOME'], 'bin/mplayer' )
    mplayer_conf_dir = '%s/%s' %( os.environ['HOME'], '.mplayer' )
    
    os.environ['media_dir'] = '%s/%s' %( os.environ['HOME'], '.mplayer/media_dir' )
    
    def __init__(self, mplayer_args=None, options=None ):
        '''
        Start mplayer first, ask questions later
        '''
        
        videofile=None
        self.instances[id(self)] = self

        if options:
            self.mpsh_options = options
        else:
            self.mpsh_options = {}

        self.loop_pos_a, self.loop_pos_b = float(), float()
        self._init_polling()
        devnull = open( '/dev/null', 'r' )

	self.mpsh_conf = self.mpsh_options.get('config', '%s/%s' %( self.mplayer_conf_dir, 'mpsh.conf' ) )

        mpcmd = [self.mplayer_binary, '-noconfig', 'all', '-include', self.mpsh_conf]
        
        if self.mpsh_options.get('ascii', False):
            mpcmd.extend( ['-vo', 'aa:driver=xv', '-monitorpixelaspect', '0.61'] ) # '-input' , 'conf=%s/input-default.conf' %self.mplayer_conf_dir, 

        if self.mpsh_options.get('shuffle', None):
            self._msg('shuffle mode enabled.\n')
            videofile, playlist = self.shuffle()
	    mplayer_args.append(videofile)
            # playlist = '%s/playlist.txt' %self.mplayer_conf_dir
	    # videofile = '%s' % open(playlist).readline().strip()

        session_cmd_in = os.environ.get('cmd_fifo', None )
        session_cmd_out = os.environ.get('out_file', None )
	
	if self.mpsh_options.get('attach') and ( session_cmd_in and session_cmd_out ):
            session_id = os.path.basename( session_cmd_in ).split('-')[-1]
            self._mplayer = subprocess.Popen( ['true'], stdin=devnull, stdout=subprocess.PIPE,
                                                                      stderr=subprocess.STDOUT, close_fds=True )
	    self._mplayer.wait()
 
            if self.attach( session_id ):
                self.mpsh_options ['attached_session'] = True
                self._msg('Attached to: %s - %s\n\n' %(session_cmd_in, session_cmd_out))
            
        else:
            session_id = '%x' %abs(self.__hash__() )

            cmd_in = '%s/mpin-%s' %( self.mplayer_conf_dir, session_id )
            cmd_out = '%s/mpout-%s' %( self.mplayer_conf_dir, session_id )
       
            if os.path.isfile(cmd_out) or os.path.isfile(cmd_in):
                rnd_suffix = ''
                for b in open('/dev/urandom').read(4): 
                    rnd_suffix += '%x' %ord(b)
                cmd_out = '%s.%s' %(cmd_out, rnd_suffix)
                cmd_in = '%s.%s' %(cmd_in, rnd_suffix)
            try:
                os.mknod(cmd_out)
                os.mkfifo(cmd_in)
            except IOError, e:
                self._msg('%s\n' %e)
                return -1

            os.environ['cmd_fifo'] = cmd_in
            os.environ['out_file'] = cmd_out            

            mpcmd.extend( ['-input', 'file=%s' %cmd_in, '-input', 'conf=%s/input.conf' %self.mplayer_conf_dir] )

	    if mplayer_args:
                print("DEBUG:" + mplayer_args.__repr__()) 
                for arg in mplayer_args:
                    mpcmd.append(arg)
	            if not arg.startswith('-') and not videofile:
                        videofile = arg
            print ("DEBUG: " + videofile.__repr__())
            os.environ["videofile"] = videofile.__repr__()

            if self.mpsh_options.get('audiofile', None):
                mpcmd.insert ( 1, self.mpsh_options['audiofile'] )
                mpcmd.insert ( 1, '-audiofile' )
        
            self._mpsh_mplayer_in = open(cmd_in, 'r+', buffering = 1 )
            self._mpsh_mplayer_out = open(cmd_out, 'rU',buffering = 1 )

            self._mplayer = subprocess.Popen( mpcmd, stdin=devnull , 
                                                     stdout=open(cmd_out, 'w', buffering = 1 ), 
                                                     stderr=subprocess.STDOUT, close_fds=True )

             

        if self.mpsh_options.get('detach', None):
            #self.suspend( timeout=0 )
            return
        
        #self.props = MPlayer.MPlayer_Properties(self)
        #self.cmds = MPlayer.MPlayer_Commands(self)
        
        if not self._mplayer.pid:
            self._msg ('No running mplayer instances found\n')
            return None      

        ret = self._readoutfile(minlines=40, timeout=1)
            
        for line in ret:
            for word in ['MPlayer', 'Playing', 'File not found', 'Fail', 'err']:
                if word in line:
                    self._msg(line,)
        self._msg ('\n',)

        if self.mpsh_options.get( 'shuffle', None ):
            self.command( 'loadlist %s %d' %(playlist, 1) )
	

    def close( self ):
        print 'closing.'
        self._clean_up()
            
    def _clean_up( self ):
        for instance in self.instances.values():
            try:
                os.remove( instance._mpsh_mplayer_in.name)
                os.remove( instance._mpsh_mplayer_out.name)
                self._msg( 'removing: %s, %s\n' %(instance._mpsh_mplayer_in.name, instance._mpsh_mplayer_out.name))
            #if not pgrep('mplayer.*%s' %self._mpsh_mplayer_in.name):
             #   self._mplayer.terminate()
              #  return True
            except Exception, e:
                print e


    def _init_polling( self ):
        self.poll_interval = self.mpsh_options.get('poll_interval', 0 )

        signal.signal(signal.SIGALRM, self._on_alarm)
        signal.alarm(self.poll_interval)

        signal.signal(signal.SIGUSR1, self._on_usr)
        signal.signal(signal.SIGUSR2, self._on_usr)
        return None

    def _on_alarm(self, sig, func=None):
        videofile = os.environ.get('videofile')
        if not videofile or videofile == 'ERROR':
            path = self.props.get_path()
            if path:
                os.environ['videofile'] = path

            signal.alarm(self.poll_interval)
            return None

        mplayer_pid = pgrep('bin/mplayer.*%s' %os.path.basename(os.path.realpath( videofile)))

        if not mplayer_pid:
            mplayer_pid = pgrep('mplayer.*%s' %os.path.basename(os.environ.get('cmd_fifo')))
            if not mplayer_pid:  
                self.suspend()
                return None
        
        if self.loop_pos_a and self.loop_pos_b:
            self.loop_a_b()
            return None
        
        signal.alarm( self.poll_interval )
        return

    def _on_usr(self, sig, func=None):
        if sig == signal.SIGUSR1:
            self.set_a()
        else:
            if self.mpsh_options.get('translate', None):
                self.translate_sub()
            else:
                self.set_b()

    def _get_sessions(self):
        mplayer_pids = pgrep('mplayer', greedy=True, verbose=True)
        mplayers = dict()

        if len(mplayer_pids) == 0:
            return None, None, None
        
        for mplayerpid in mplayer_pids:
            pid, cmdline = mplayerpid
            ppid = get_ppid( pid )
            
            has_cmd_fifo = '-input file=' in cmdline

            if has_cmd_fifo:
                cmd_in = cmdline.split('file=')[1].split()[0]
                cmd_out = cmd_in.replace('mpin', 'mpout')
                session = cmd_in.split('-')[-1]
            else:
                cmd_in = os.path.join( '/proc/', pid, 'fd', '0' )
                cmd_out = os.path.join( '/proc/', pid, 'fd' , '1' )
                session = 'foreign-%s' %pid
          
            if not ppid in mplayers.values():
                mplayers[ session ] = ( pid, ppid, cmd_in, cmd_out, cmdline )
        
        #self._msg('mpsh/mplayer instances:\n')
        #for k in mplayers.keys():
         #   self._msg( 'pid: %s\t %s\n' %(k, mplayers.get(k)))
        return mplayers

    def _readoutfile(self, minlines=1, timeout=0.5):
        ret = []
        time_spent = 0
        interval = 0.02
        lines_read = len(ret)

        while time_spent < timeout and ( len(ret) < minlines or len(ret) > lines_read ):
            lines_read = len(ret)
            for line in self._mpsh_mplayer_out.readlines():
                ret.append(line)
                
            time.sleep(interval)
            time_spent += interval
            #if len(ret) > lines_read:
             #   self._msg('debug _readoutfile: len(ret) %s > lines_read %s:' %(len(ret), lines_read))

        return ret

    def _msg(self, message):
        if not self.mpsh_options.get('detach', False):
            try:
                sys.stderr.write(message)
            except IOError, e:
               print(e)

    def _wait_animation( self, timeout=5 ):
        t_start = time.time()
        while not (time.time() - t_start) >= timeout:
            for c in ['\\ ', '|', '/', '-' ]:
                self.osd_show_text(c)
                time.sleep(0.02)
        return              

    def get_xid( self, window_title=None ):
        if not window_title:
            window_title = self.props.get_filename()
        try:
            xidproc = subprocess.Popen( ['xwininfo', '-wm', '-name', window_title ], stdout=subprocess.PIPE, stderr=open('/dev/null','w') )
            xid = eval( xidproc.stdout.readlines()[1].split()[3] )
            return xid
           
        except Exception, e:
            #self._msg( e )
            return None

    def attach( self, session_id=None ):
        
        sessions = self._get_sessions()
	#self._msg ( 'Active sessions: %s\n' %sessions.values() )

        if not session_id:
	    keys = sessions.keys()
	    keys.remove( '%.2x' %abs( self.__hash__()) )
            session_id = keys[0]

        if session_id:
            cmd_in = '%s/mpin-%s' %( self.mplayer_conf_dir, session_id )
            cmd_out = '%s/mpout-%s' %( self.mplayer_conf_dir, session_id )
          
            if not ( os.path.exists( cmd_in ) and os.path.exists( cmd_out ) ):
                mplayer_pid = sessions[ session_id ][0]
                proc_path = os.path.join( '/proc/', mplayer_pid, 'fd' )

                for fd in os.listdir( proc_path ):
                    link = os.readlink( os.path.join( proc_path, fd) )

                    if not 'deleted' in link: 
                        continue

                    filename = link.split()[0]
                    if os.path.realpath( cmd_in ) == filename:
                        os.symlink( os.path.join( proc_path, fd), cmd_in )
                        continue

                    if os.path.realpath( cmd_out ) == filename and not os.path.exists( cmd_out ):
                        os.symlink( os.path.join( proc_path, fd), cmd_out )
            try:
                self._msg( 'Attaching to session: %s\n' %session_id )
                self._mpsh_mplayer_in = open(cmd_in, 'r+', buffering = 1 )
                self._mpsh_mplayer_out = open(cmd_out, 'rU',buffering = 1 )
		self._mpsh_mplayer_out.seek(0,2) 
                
            except OSError,e:
                self._msg( e )
            
            # self._mplayer.pid = int( sessions[ session_id ][0] )
            os.environ['cmd_fifo'] = cmd_in
            os.environ['out_file'] = cmd_out
            
            return True
        
        if len( mplayers.keys() ) == 1:         
            print 'feeling lucky? punk'
            return int(mplayers.keys()[0]), cmd_in, cmd_out
        else:
            print 'foo'

        return None

   
    def command(self, command, *args):
        """ Very basic interface [see populate()]
        Sends command 'command' to process, with given args
        """
        alarm = signal.alarm(0)
        signal.alarm( alarm + self.poll_interval )
        
        cmd = '%s%s%s\n'%(command,
            ' ' if args else '',
            ' '.join(repr(a) for a in args)
            )
        self._mpsh_mplayer_in.write( cmd )

        q = ''
        
        if 'quit' in cmd or 'osd_show_text' in cmd:
            for line in self._mpsh_mplayer_out.readlines(): 
                return line.strip()
        
        if 'get_' in cmd:
            q = cmd.replace('get_','').replace('property','').strip()
            q = q.strip('"\'')
            got_ans = False
            max_tries = 3

            while not got_ans and max_tries > 0:
                ret = self._readoutfile(minlines=1,timeout=0.5)
                for line in ret:
                    if 'ANS_%s' %q in line or 'ANS_%s' %q.swapcase() in line:
                        got_ans = True
                        return line.strip().split('=')[-1]
                    else:
                        if 'ANS_' in line and 'get_' in cmd:
                            got_ans = True
                            return line.strip().split('=')[-1]
                max_tries -= 1     
            if not got_ans:
                return None
        else:
            ret = self._readoutfile(minlines=1,timeout=0.1)    

        if len(ret) == 0 and  not ( 'loop a-b' in cmd or 'osd' in cmd) :
           self._msg ('==== %s ====\n' %cmd.rstrip() )
           return None       
        else:
            for line in ret:
                for word in ['Fail', 'Err']:
                    if word in line:
                        return 'mpsh_debug command: %s' %line.strip()
                   
                self._msg('%s\n' %line.strip())
            
        return None

    def set_a(self, time_pos_a = float()):
        if not time_pos_a:
            tp = self.props.get_time_pos()
            if not str(tp)[0] in str(range(0,10)):
                self._msg('debug set_a: %s\n' %tp)
                return -1
            self.loop_pos_a = float(tp)
        else:
            self.loop_pos_a = time_pos_a
	self.poll_interval = 10
        self.osd_show_text('loop pos a: %.2f' %self.loop_pos_a)

    def set_b(self, time_pos_b = float()):
        if not time_pos_b:
            try:
                self.loop_pos_b = float(self.props.get_time_pos())
            except Exception,e:
                print e
        else:
            self.loop_pos_b = time_pos_b
	
	alarm_secs = signal.alarm(0)
	loop_len =  int( self.loop_pos_b - self.loop_pos_a )

	if alarm_secs > loop_len:
	    signal.alarm( loop_len )
	else:
	    signal.alarm( alarm_secs)

        self.osd_show_text('loop pos b: %.2f' %self.loop_pos_b)
        self.loop_a_b()

    def loop_load(self, filename=None, loopdb_fn='%s/loopdb.json' %mplayer_conf_dir, start_loop=True):
        import json
        
        if not filename:
            # if not os.environ.has_key('videofile'):
            os.environ['videofile'] = self.get_property('path')
            filename = os.path.basename( os.environ['videofile'] )
        else:
            filename = os.path.basename( filename )
        
        try:
            loopD = json.load(open(loopdb_fn, 'r+'))
        except:
            return
            
        if not loopD:
            return
        else:
            if start_loop:
                if loopD.has_key( filename ):
                    time_pos_a, time_pos_b = loopD.get(filename)
                    self.poll_interval = 10
		    return self.loop_a_b( time_pos_a, time_pos_b )
                else:
                    return
            return loopD

    def loop_save(self, loopdb_fn='%s/loopdb.json' %mplayer_conf_dir ):
        import json
        
        loopD = self.loop_load( start_loop=False )
        if not loopD:
            loopD = {}
        
        filename = os.path.basename( os.environ['videofile'])

        try:     
            loopdb = open(loopdb_fn, 'w')
            loopD[ filename ] = self.loop_pos_a, self.loop_pos_b
            json.dump( loopD, loopdb, indent=4 )
            loopdb.close()
            return
        except IOError, e:
            self._msg( e )
            return -1
      

    def loop_a_b(self, time_pos_a = None, time_pos_b = None, reset = False):
        alarm = signal.alarm(0)

        if reset:
            self.loop_pos_a, self.loop_pos_b = float(), float()
            self._msg('loop reset\n')
            alarm = 10
            return None
                           
        if time_pos_a and time_pos_b:
            self.loop_pos_a, self.loop_pos_b = time_pos_a, time_pos_b
         
        if self.loop_pos_a and self.loop_pos_b:
            time_pos = None
            loop_len = self.loop_pos_b - self.loop_pos_a
            if time_pos_a and time_pos_b:
                progress =  '>--%.2fs---' %loop_len
                #self.osd_show_text('loop a-b %.2f%s%.2f' %( self.loop_pos_a, progress, self.loop_pos_b) )
            while not time_pos:
                try:
                    time_pos = float(self.props.get_time_pos())
                except Exception,e:
                     print e
                     time.sleep(0.1)
            
        if time_pos >= self.loop_pos_b or time_pos <= self.loop_pos_a:
            self.set_property('time_pos', (self.loop_pos_a))
            progress = '----<<----'
        else:
            time_left =  int(self.loop_pos_b - time_pos)
            progress = '%s%s%s' %( (10 - int( 10* (float(time_left)/loop_len))) * '=', '>', (int(10 * (float(time_left)/loop_len))-1) * '-' )
            if (time_left) < 20 or loop_len < 20:
                alarm = 1
                if time_left <= 10:               
                    progress = '%s%s%s' %( (( 10 - time_left) * '='), '>', ((time_left-1) * '-'))

        self.osd_show_text('loop a-b %.2f%s%.2f' %( self.loop_pos_a, progress, self.loop_pos_b), 5000)

        if alarm > 0:
            signal.alarm(alarm)
        else:
            signal.alarm(self.poll_interval)
        
        return True
             
    def shuffle(self):
        """
        returns a shuffled list of files residing in media_dir, recursively,
        and a random item (string) from this list 
	"""

        media_dir = os.environ.get('media_dir', '/tmp')
        playlist = '%s/playlist.txt' %self.mplayer_conf_dir
	vidlist = []
        
        for vid in open(playlist).readlines():
            vidlist.append(vid.strip())
	
	#for base, dirs, files in os.walk( media_dir):
         #   for vid in files:
          #      vidlist.append( os.path.join(base, vid))

        random.shuffle(vidlist)

        # playlist = '%s/playlist.txt' %self.mplayer_conf_dir

        f = open ( playlist, 'w')
        for vid in vidlist:
            f.write( '%s\n' %vid )
        f.close()

        random_vid = os.path.join( media_dir, random.choice( vidlist ))
        # vid = os.path.join( media_dir,  vidlist[-1])
        
        return random_vid, playlist
           
    def get_subtitles( self ):
        ''' 
        find a subtitle on opensubtitles.org 
        '''
        import getsub2
        signal.alarm(0)

        videofile = self.get_property('path')
        sd = getsub2.SubtitleDownloader( filename=videofile )
        subfile = sd.get_subtitle()
        if subfile:
            self.menu('cancel')
            self.suspend()
            return subfile
        else:
            signal.alarm(self.poll_interval)
            return None

    def get_subfilename(self):
        ''' 
        return full path of loaded subtitle 
        '''

        sub_filename = os.environ.get('sub_filename', None)

        if sub_filename:
            return sub_filename

        saved_pos = self._mplayer.stdout.tell()
        self._mplayer.stdout.seek(0)
        subinfo = [ line for line in self._mpsh_mplayer_out if 'SUB' in line ]

        for line in subinfo:
            if line.startswith('ID_FILE_SUB_FILENAME'):
                sub_filename = line.split('=')[-1].strip()
            else:
                if line.startswith('SUB'):
                    sub_filename = line.split(' ', 5)[-1].strip()
        
        self._mplayer.stdout.seek( saved_pos )

        if sub_filename:
            os.environ['sub_filename'] = sub_filename
    
        return sub_filename                    
    
    def translate( self, text=None, current_subtitle=False ):
        from translator import Translator
        t = Translator()
        translated_text = t.translate( text=text )
        return translated_text

    def translate_sub( self ):
        def HMStos( HMS ):
            h,m,s = HMS.split(':')
            seconds = (float(h) * 3600) + (float(m) * 60) + float(s.replace(',','.'))
            return seconds
            
        time_pos = float(self.get_time_pos())
        time_pos_min = float(time_pos - 3)
        sub_filename = os.environ.get('sub_filename')

        if not sub_filename:
            sub_filename = self.get_subfilename()

        os.environ['sub_filename'] = sub_filename

        f = open(sub_filename)
        subtitle = f.readlines()
        f.close()      

        sub_matches = []
        for l in subtitle:
            if '-->' in l:
                sub_start, sub_end = l.strip().split('-->')
                sub_start_secs = HMStos( sub_start )
                sub_end_secs = HMStos( sub_end )
                
                print sub_start, sub_end, sub_start_secs, sub_end_secs
                
                if sub_start_secs >= time_pos_min and sub_start_secs <= time_pos + 1:
                    index = subtitle.index( l )
                    sub_matches.extend( subtitle[ index + 1: index + 3] )
          
        for match in sub_matches:
            tmatch = self.translate( match ).encode()
            self.osd_show_text( tmatch ,2000)
            time.sleep(2)
            for i in range( 0, len(tmatch), 1):
                self.osd_show_text(tmatch[i:],200)
                time.sleep(0.01)
        

    def savefd(self):
        '''
        save flash stream to disk
        '''
        from shutil import copyfile
        
        src = self.command('get_property path')
        base, ext = os.path.splitext(os.path.basename(src))
        if not len(ext) == 4:
            codec = self.command('get_video_codec').strip('\'')
            #ext = '.%s' %codec[-3:].swapcase()
            ext = '.flv'
        
        dst = os.path.join(os.environ.get('media_dir'), '%s%s' %(base, ext))
        
        while os.path.exists(dst):
            dst += ('.mpsh_savefd_dup')
        self._msg ('\n\nSaving: %s\n\n' %(dst))
        
        copyfile(src,dst)
        return dst
    
    def suspend(self, timeout=10):
        signal.alarm(0)
        self._msg ('Suspend. mpsh will exit in %s seconds.\n' %timeout)

        if not os.isatty(sys.stdin.fileno()):
            time.sleep(timeout)
            exit()

        i = None
        for s in range(0, timeout):
            i, o, e = select.select( [sys.stdin], [], [], 1)
            if(i):
                self._msg ('Suspend interrupted %s\n' %sys.stdin.read(1))
                signal.alarm(self.poll_interval)
                break
        if not i:
            exit()

    class MPlayer_Commands(object):
        def __init__(self, clss):
            self._cmd_ref = dict()
            self._populate_commands(clss)
        
        def _fn_factory(self, clss, command, *args):
            def _gen_fn(*args):
                return clss.command(command, *args)

            _gen_fn.__name__ = command
            _gen_fn.__doc__= '%s\nType: %s' %( command, ' '.join(self._cmd_ref[command]))
            
            return _gen_fn
        
        def _populate_commands(self, clss):
            ''' 
            populate mplayer command reference
            '''

            cmdsproc = subprocess.Popen([MPlayer.mplayer_binary, '-input', 'cmdlist'],
                                      stdout=subprocess.PIPE)
            cmdsproc.wait()
            cmdsraw = cmdsproc.stdout.readlines()
            
            for line in cmdsraw:
                args = line.strip().split()
                self._cmd_ref [ args[0] ] = args[1:]
                       
            for cmd in  self._cmd_ref.keys():
                _pop_fn = self._fn_factory(clss, cmd, *args)
                self.__dict__[ cmd ] = _pop_fn
                clss.__dict__[ cmd ] = _pop_fn

    class MPlayer_Properties(object):
        def __init__(self, clss):
            self._prop_ref = dict()
            self._populate_properties(clss)
        
        def _populate_properties(self, clss):
            ''' 
            populate mplayer property reference
            use to get and set mplayer properties:
            p.properties.get_path(),
            p.properties.set_framedropping(1)
            '''

            props_proc = subprocess.Popen([MPlayer.mplayer_binary, '-list-properties'],
                                      stdout=subprocess.PIPE)
            props_proc.wait()

            propsraw = props_proc.stdout.readlines()

            self.__mplayer_version__ = propsraw[0].split()[1]

            for line in propsraw[4:]:
                line = line.replace('String list', 'String_list')
                line = line.strip().split()
                if not len(line) < 2 and not line[0].startswith('Total'):
                    self._prop_ref [ line[0] ] = line[1:]
          
 
            for key in self._prop_ref.keys():
                type, min, max =  self._prop_ref[ key ]
                
                def _get_property(key=key ):
                    return clss.command('get_property %s' %key)

                setattr(self, 'get_%s' %key, _get_property )
                #setattr(clss, 'get_%s' %key, _get_property )
                _get_property.__name__ = 'get_%s' %key
                _get_property.__defaults__ = (key,)
                _get_property.__doc__ ='Get property %s\nType: %s\tMin: %s\tMax: %s' %( key, type, min, max )
                
                if not 'No' in min:
                    def _set_property(args, key):
                        return clss.command('set_property %s %s' %(key, args) ) 

                    setattr(self, 'set_%s' %key, _set_property )
                    #setattr(clss, 'set_%s' %key, _set_property )
                    _set_property.__name__ = 'set_%s' %key
                    _set_property.__defaults__ = ('%s' %key,)
                    _set_property.__doc__ ='Set property: %s\nType: %s\tMin: %s\tMax: %s' %( key, type, min, max ) 


if __name__ == '__main__':

    if '--pty' in sys.argv: 
        if not os.isatty(sys.stdin.fileno()):
            import pty
            mpsh_path = os.path.abspath(sys.argv[0])
            # args = [ 'screen','-O', '-S','mpsh', 'python', mpsh_path ]
            args = [ 'python', mpsh_path ]
            args += sys.argv[1:]
            pty.spawn(args)
            # explicit exit to prevent dropping back to tty challenged parent
            exit()
        else:
            sys.stdout.write('tty already allocated, no need to get pty\n')

    
    pid = os.getpid()
    
    if not os.isatty( sys.stdin.fileno()) or '--detach' in sys.argv:
	print 'DEBUG: notatty!'
        child_pid = os.fork()
        print 'fork: ', os.getpid(), pid, child_pid
        if pid == os.getpid():
            #os.close( child_fd )
            exit()
                
    import mpsh_completer
    from code import InteractiveConsole

    sys.ps1='p~> '
    mpsh = InteractiveConsole()

    _mpsh_options = dict( {'pty':0, 'attach':0, 'detach':0, 'getsub':0, 'loop':0, 'shuffle':0, 'help':0,
                              'audiofile':0, 'id':0, 'ascii':0, 'translate':0 } )
     
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--') and arg[2:] in _mpsh_options:
                _mpsh_options[ arg[2:] ] = True
                sys.argv.remove(arg)
            
            if arg in ['-audiofile', '-config', '-id']:
                _mpsh_options[ arg[1:] ] = sys.argv[ sys.argv.index( arg ) + 1 ]
                sys.argv.remove( arg )
                sys.argv.remove(_mpsh_options[ arg[1:] ])

            
        mplayer_args = sys.argv[1:]
         
        p = MPlayer( mplayer_args, _mpsh_options )
    else:
        p = MPlayer( options=_mpsh_options )

    mpsh.locals = locals() 
    
    if not os.isatty( sys.stdin.fileno() ) or _mpsh_options['detach']:
	p._mplayer.wait()
    else:
	p.props = MPlayer.MPlayer_Properties(p)
	p.cmds = MPlayer.MPlayer_Commands(p)
 
	if _mpsh_options['getsub']:
	    p.poll_interval=10
	    debug_osdbinfo = p.get_subtitles()
        
	if _mpsh_options['loop']:
	    if not p.loop_load():
	        p.set_a()
            p.menu('cancel')
    
        if _mpsh_options['translate']:
            p._msg('google translate enabled.\npress [ ? ] to attempt subtitle translation.\n')
            time.sleep(3)
            p.menu('cancel')

 	mpsh.interact(banner='mpsh %s - mplayer %s\n' %(__mpsh_version__, p.props.__mplayer_version__)) 

    p._clean_up()
    p._mplayer.terminate()
    exit(0)

