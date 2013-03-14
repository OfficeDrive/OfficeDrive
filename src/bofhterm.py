#!/usr/bin/python

import os, sys
import string
import getopt
import pygtk,gtk
import vte

class Terminal(vte.Terminal):
    audible = 0
    background = None 
    blink = 0
    command = None
    emulation = 'xterm'
    font = 'Terminus 10'
    scrollback = 1000
    transparent = 0
    visible = 0    
# Let the user override them.
    (shorts, longs) = getopt.getopt(sys.argv[1:], 'B:Tabe:f:n:t:v', ['background', 'transparent', 'audible', 'blink', 'command=', 'font=', 'scrollback=', 'terminal=', 'visible'])
    for argpair in (shorts + longs):
        if ((argpair[0] == '-B') or (argpair[0] == '--background')):
            print 'Setting background image to `' + argpair[1] + '.'
            background = argpair[1]
        if ((argpair[0] == '-T') or (argpair[0] == '--transparent')):
            print 'Setting transparency.'
            transparent = not transparent
        if ((argpair[0] == '-a') or (argpair[0] == '--audible')):
            print 'Setting audible bell.'
            audible = not audible
        if ((argpair[0] == '-b') or (argpair[0] == '--blink')):
            print 'Setting blinking cursor.'
            blink = not blink
        if ((argpair[0] == '-e') or (argpair[0] == '--command')):
            print 'Running command `' + argpair[1] + '.'
            command = argpair[1]
        if ((argpair[0] == '-f') or (argpair[0] == '--font')):
            print 'Setting font to ' + argpair[1] + '.'
            font = argpair[1]
        if ((argpair[0] == '-n') or (argpair[0] == '--scrollback')):
            scrollback = string.atoi(argpair[1])
            if (scrollback == 0):
                scrollback = 100
            else:
                print 'Setting scrollback size to ' + str(scrollback) + '.'
        if ((argpair[0] == '-t') or (argpair[0] == '--terminal')):
            print 'Setting terminal type to `' + argpair[1] + '.'
            emulation = argpair[1]
        if ((argpair[0] == '-v') or (argpair[0] == '--visible')):
            print 'Setting visible bell.'
            visible = not visible

    bofh_next_level_colorscheme = { 'bg' : gtk.gdk.Color('#2e2e2e'), 'fg' : gtk.gdk.Color('#cdF3cD') }

    def __init__(self):
                                
        vte.Terminal.__init__(self)
        self.set_size(80,24)
        
        w = gtk.Window()
        w.set_size_request(800,480)
        #w.set_default_size( 800, 320 )
        w.set_resize_mode(1)
        w.set_icon( self.load_icon_blob() )
        w.connect( 'destroy', self.child_exited_cb)

        self.set_cursor_blinks(self.blink)
        self.set_emulation(self.emulation)
        self.set_font_from_string(self.font)
        self.set_scrollback_lines(self.scrollback)
        self.set_audible_bell(self.audible)
        self.set_visible_bell(self.visible)

        self.connect('child-exited', self.child_exited_cb)
        self.connect('restore-window', self.restore_cb)
        #self.connect('resize-window', self._debug_action, 'resize-window')
 
        self.menu = gtk.Menu()
        acc_group = gtk.AccelGroup()

        menu_item = gtk.MenuItem( 'font_size +1' )
        menu_item.connect( 'activate', self.set_font_size, 'increase' )
        menu_item.add_accelerator( 'activate', acc_group, ord( '+' ), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE )
        self.menu.append( menu_item )

        menu_item = gtk.MenuItem( 'font_size -1' )
        menu_item.connect( 'activate', self.set_font_size, 'decrease' )
        menu_item.add_accelerator( 'activate', acc_group, ord( '-' ), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE )
        self.menu.append( menu_item )
        
        menu_item = gtk.MenuItem( 'copy' )
        menu_item.connect( 'activate', self._copy )
        menu_item.add_accelerator( 'activate', acc_group, ord('c'), gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK, gtk.ACCEL_VISIBLE )
        self.menu.append( menu_item )

        menu_item = gtk.MenuItem( 'paste' )
        menu_item.connect( 'activate', self._paste )
        menu_item.add_accelerator( 'activate', acc_group, ord( 'v' ), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE )
        self.menu.append( menu_item )

        self.connect( 'button-press-event', self.button_press, self.menu )
        w.add_accel_group( acc_group )

        if (self.command):
            cmd = self.command.split('"',2)
            if len(cmd) > 1:
                cmd_quoted_arg = cmd.pop(-2)
                cmd_arglist = cmd[0].split()
                cmd_arglist.append( cmd_quoted_arg )
            else:
                cmd_arglist = self.command.split()
        
            cmd_base = cmd_arglist[0]
            child_pid = -1
            child_pid = self.fork_command( cmd_base , cmd_arglist )
            print 'fork: %s, %s' %( cmd_base, cmd_arglist )
        else:
            # Start up the default command, the user's shell.
            child_pid = self.fork_command()
            self.command = os.environ.get( 'SHELL', '-' )
        
        if not child_pid:
            print 'fork failed'
            exit()

 	screen = self.get_screen()    
                
        if self.is_composited():
            colormap = screen.get_rgba_colormap()
        else:
            colormap = screen.get_rgb_colormap()
        
        if (self.background):
            self.set_background_image_file(self.background)
        #else:
            self.set_background_image(w.get_icon())
        self.props.background_opacity = 0.88
        #self.props.background_saturation = 0.125
        
        
        if (self.transparent): # fake transparency
            self.set_background_transparent(gtk.TRUE)
        w.set_colormap( colormap )
        w.set_title( 'BOFHterm: %s - %d' %( self.command, child_pid ) )

        #self.sw = gtk.ScrolledWindow()
        #self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        #self.sw.set_policy(-1,-1)
        #self.sw.add( self )
        w.add(self)
        w.show_all()
	

        clipboard = self.get_clipboard(gtk.gdk.SELECTION_CLIPBOARD)


        style = self.rc_get_style().copy() 
        self.menu.show_all()
               
        self.set_style(style)
               
        self.set_color_background(self.bofh_next_level_colorscheme['bg'])
        self.set_color_foreground(self.bofh_next_level_colorscheme['fg'])

        #self.set_color_background(style.base[gtk.STATE_NORMAL])
        #self.set_color_foreground(style.fg[gtk.STATE_ACTIVE])
	##self.set_color_highlight(style.base[gtk.STATE_PRELIGHT])
        ##self.set_color_cursor(style.base[gtk.STATE_SELECTED])
        

        
    def _copy( self, *args ):
        self.copy_clipboard()

    def _paste( self, *args ):
        self.paste_clipboard() 
        
    def _debug_action( self, action, string ):
        print 'action: %s - %s' %(action.get_name(), str(string))

    def selected_cb( self, terminal, column, row, cb_data ):
        if (row == 15):
            if (column < 40):
                return 1
        return 0

    def button_press( self, parent, event, data ):
        # print parent, event.button, event.time
        if event.button == 3:
            parent.menu.popup( None, None, None, event.button, event.time )
        pass
    
    def set_font_size( self, widget=None, change_type=None, new_font_size=None ):
     
        font = self.get_font()
  
        if new_font_size:
            font_size = new_font_size
        else:
            font_size = font.get_size()

        if change_type:                
            if change_type == 'increase':
                font_size += 1024
            else:
                if change_type == 'decrease':
                    font_size -= 1024

            
        font.set_size( font_size )
        self.set_font( font )
    
        return font_size



    def restore_cb(self, terminal):
        (text, attrs) = t.get_text(selected_cb, 1)
        print 'A portion of the text at restore-time is:'
        print text

    def child_exited_cb( self, terminal ):
        gtk.main_quit()

    def load_icon_blob( self ):
        icon_blob = '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x000\x00\x00\x000\x08\x06\x00\x00\x00W\x02\xf9\x87\x00\x00\x06\xf6IDATh\xde\xedYkL\x9b\xe7\x15>\xe7\xfd.\x0e&\xd8\xc6\xd0\xc2\x9c8Ik\x92\xa9i\x88\xa6J]`R\xb3&U\x16\xaa\xb4\nk\xb2\x1f\xd5D\xa4\xf5\x92T\x93\xda\xa8\xfb1Z\xadj\xa7\xb6\x93\xd2\x1fM\x08i&M\x95\xa7\xa5\x89\x1a)\x856-\xa5\r*U\xa6\x16\x08\xa0\xd4\\\n\x94$\x985!6`\x8c\xb1\x01_>\xfb\xfb\xde\xb3\x1f\xb6\x91GH\xe7\x18\xb3\x0e\x89\xf7\x8f\xbf\xcby\xcfw\x9esy\xcf\xc5\x00+ke-\xcb%d\x8b\x11\xfb1\xa4\x7f\xe6\xadb\xeb\xb2\x06\x10\x95\xc7od\x8b\x17.\x95\x90\x13\xef\xbcc\xd5<\x1e\xbb\x1a\x08\xe4\xae\xde\xb9\xf3\x80i\xef^\xe7R|gI,\x10lk\xb3\x82\xaa\xd6\xcf~\xf9\xe5\xaepG\xc7/"==g\xa7\xea\xea6-\xc5\xb7\xd2\xb6\x80\xf7\xddw\x0b\x90\xa8\x1ad9(\x18\x0co\xeb\xcb\xca\x82\xb2\xc5B\xf3\xe9\x02\x8d\x8d?\x89|\xfb\xed\xdf\x82\xad\xad\x8fO\x0e\x0er\xc69\xe6\xe5\xe7\xc7V\x95\x96\x9e\xd5\xd9l\x7f,z\xe5\x15\xcfB\xfcg\xbe\xf8B\xe4\x91H\xb528x\x97n\xeb\xd6#\xc6\xdd\xbb\xc7\xd2\x91KLK\xa3\x0e\x87y\xb6\xb9\xf9x\xc4\xe1x\x12\x05A\x95\xef\xbbo\x8d\xe9\x89\'\x0e\xce\xa7\x9bnl| \xd4\xd5\xf5z\xa4\xb5u\xcf\xd4w\xdfqY\x14\x11\x10!\xe8\xf3I\xc2\xd0\xd0\x01\x94\xa4\xd5\xae\xe7\x9f?\xbc\xe6\xc4\tW\xea\xbe\xd9\xf6vS\xd8\xe18\xa2\xf4\xf4<\xaby<L((\xd8\x07\x00\xd6\xac\x00\xf0\x7f\xfc\xb1q\xb6\xb9\xf9/\x91\xae\xae\xdf\x8evv\x12\x03\x90\xee\x0e\x85\x9e\r44T\x84\xbb\xbal\xc5\xaf\xbe\x1aK\xd2*N\xe7\x93Q\xa7s\x8f\xbb\xaf\x8f\xe7\xadZ\xc5\x92\xe6a\x8c\x91od\x04\xcc\x92\xb4\xcf\xb0wo\x00\x00\x9eN\xb1\xd8\xea`K\xcbkJO\xcf\xa1\xd1\xb66b\x9a\x06Q\x97\xcb2\xf5\xc1\x07!}Y\xd9F\x9d\xd5\xeaZT\x0c\xa8cco+\x1d\x1d\xcfM\xb4\xb7S\x0ec 3\x06S\xbd\xbd0YSSD\x9a\xf6\x9a\xbf\xae.\'I\x1b\xbat\xa9\t\x19\xeb+\xde\xb6\x8d\xa1\xa6\x01\x11\x01\x11\x81@\x04\xf9\x9b7\x03\x0f\x06\xff)\x98\xcd\x81T\xfe1\xb7\xfb-\xa5\xb3\xf3\xb0\xa7\xa5\x85V!\x82$\x8a0\xeb\xf5\xe2dMMN\xf8\xf2\xe5\xbeE\x05\xf1\xa4\xdd\xfeF\xa4\xbb\xfbi\xf77\xdf\x90N\x14\x11\x11\x91!""\x92\xef\xfau)z\xed\xda\x9f\xb4\x99\x99\x17\x93\xf4\xeb\xcf\x9em\xb6\xda\xed\xa5\x05O=\xd5\x8e\x9a\x06\x00\x00\x9c\x08\x18"\x9a*+;6vt\xec0WU\xfd!E\xfb\xfb\xa3N\xe7\xef\xdd\x9d\x9d\xa0\x13EH\xf0\'\xc6\x18\x06\xc6\xc6\xc0g\xb7\x1bF_z\xe9\x85\x8c\x01L74\xa8\x8a\xd3\t\xa6\x82\x02 \xce\xe74\xca\x88 77\x17b.\x17\x08\x06C\xe5-\'\x03\xe2\xad\xaeIt\xcb\xb3Ho\xef\x16>33\xc7?NF\x08\x00\xa4\xcf\xcb#R\x14\x16\x1d\x1e\xc6\x8cc\xa0\xf0\xf0\xe1\xeb\x80\xd8\x17\xee\xea\xda\xe8\xad\xad\xd5\xc5\x04\x01\x08\x80$\xc6\xd0\xf4\xd8c\xb3\xfa\x87\x1er\x1b+*~\xbe\x80\xb0\x90\xce\xb3\xa2\x97_\xfe\xb3\x1a\x08\x9c\xf6\x9f9\xd3\xef9zT\x17\xa38\x11\xaa*\x1aw\xed\n\xe7\xee\xdc9,\xad]{\x11\xce\x9d\xcb\xcc\x02y;v\xfc#\xef\xe1\x87Ke\x9bm\x804\x8d\x08\x00\x08\x00A\x14I\xba\xf7\xde\x01cE\xc5O\x17]\x14\x19\x0c\xff\x92l\xb6\xee\xa4\xec\x04\x80\x02\x00I\xeb\xd7\x0f\x18\x1f}t\x8b\xbe\xb4\xb4w\xf1\x89\x8cs\x8d\x18\xc3\x94\xc4\x81\xc8XV\x92 "r\x00`8??\xd1Bf\xccf&N\xf8\xec\x8f\xbd\x18,\xf3\xb5\x02`\x05\xc0\n\x80\x15\x00+\x00V\x00d\xb8\xf3\x0e\xb6bz\x9dk\x9a\xd5C\x96\x00 \xde\xf6k\xb4\x90\xc0\xffM\xba\x0c\x84\xcf\x1c\x00\x11h\x13\x13\xeb\x03\x8d\x8d\x1b\x16z\xady<j\x94s\xa0x\xb1\x16\x7f\xe6\xf7\xdf\xe3\xff\xf0\xc3\x05\xabW\xd5\xedVc\xaa\x9a\xb6\xa52\x02\x80D\x80\x89jT\x8b\xc5h\xea\xa3\x8f\n\x95\xabW?\x99\xb9p!\xe7?\xe6A\xb5\xb5\xbf\xf3\xd7\xd7\x97\xa1$\xcd\xd1\xc78\'\xff\xf9\xf3\xe6\xa8\xd3Y7\xdd\xd4\xa4O1\n\xf3\x9d>\xfd\xa9\xff\xdc\xb9r\x92e\xc2\xa5\xb2\x00"2UQ8\x01\x10"\x82\x86\x08\xc1\xf1q\x9c\xae\xaf/\r\xf7\xf7_\x8e\x0c\r\x15\x00\x00\x8c\x1f9r2x\xe1\xc2\xdf\xa7\xfb\xfb\x89\t\x02 b\xdc\x02\x88\x10\xf4zq\xfa\xfc\xf9-\xe1\xeenGxx\xd8\x0c\x00\xe0\xad\xad}?p\xe6\xcc\x9e\x99k\xd7\x8816g\xad\x98\xa6\x01)JZ\x00\xc44\x83\xab\xd5\xb4}\xfb\x03^\x87#\xde\xa4#"\x02\xd0\xd4\xcd\x9b$|\xf5\xd5\xe6\xd8\xc8\xc8_\xc7\xde|\xd3\x1a\xee\xec,\xf7\x0c\x0c\x90,\xde\xc2\x16\x05D\xf2\xbb\xdd\x84\x17/nRGG\xed\x9e\xa3G\xcd\xa1\xd6\xd6\xed\xbe\xc1A\x12%i.L\x88\x88V[\xad(\x97\x94\xf4dm\xb0\x15hh\xb8K\xb9r\xe5\xd8tS\xd3of\x87\x86dLh\x17\x88\x80\x13Q\xde\x9a5\xa8)\n\x04\'&@`\x0c\x00\xe3\xfd\x08.\xe0\xd3\xaa\xa6\x91\xc1bAD\x84\x90\xdbM<>$\x98\x13^o6c\xee\xb6m\x07,\xc7\x8f\xb7\xa1 8\xb3\x02 1|*R\xfa\xfaN\xf9\xde{ow\xf0\xe6M\x02\xc6\x80!"\x11\x81\xc69 "\x08\x8c\xddV\xf0\x84\x86\t\x11QK\x0c\x08\x84\xb8\xdb\x10\x11!\xe7\x9crrr \xbf\xaa\x8a\xe7<\xf8\xe0\xfd\x86G\x1e\xb9r\x1by)\xe3\xe1.\x11\x15\x8fVW\x7f\x1alo\xdf\xaa\xb8\\\xa2\x8a8\x07\x02RN\x9c\xa4;$\xef\x93\xd7\xa9\xbfIzN\x04\xc49\xe5\x16\x16\xa2q\xdf>\xc8?x\xb0X\xce\xcf\x1f\xbf]\x0b\r\x00\xda\x1d\xc7@J0\x8f\xa9\x9c\x97\xfbjj>\x0f|\xf6\xd9/\xd5\xef\xbf\x175M#L(\x82R\x12W*\x18D$\xce90\xc6\x10\xe2\xda\'\x00@5~(\xa0a\xdd:\xd4\x97\x97\xdb\x8b\xaa\xab\x9f\xf1\x15\x17\xdf\x91R3\x1a\xaf{\x8f\x1d\x93A\xafo\x08\xb5\xb4\xfcJ\xf1\xf9\x80%\xfc>y\x8ek\x1e\x0f\x84<\x1e\xc2\x04\n$"\x9d\xd1H\xc0\xf9\x98`0\x14\xa0\xc9\xa4\x03\x00\xe0\xd1(0D0VV\x86\n\x0f\x1d\xcaUn\xdc`\xbau\xeb~\xa8\xd9\x96\x00 \xb6\xe4\xf5\xc9\xe4\xa9S\x97\x066l\xa0\x9e\x92\x12\xea\xb6\xd9h`\xd3&>q\xe2\x84\xd7{\xf2\xe4\xcfB\xfd\xfd\xbf\x9eO?UWww\x9a\xca\x963:F\xeftI\x16\x8b\x12\xd34@Q\x04d\x0cb\x8a\x82\x82\xc9\xd4o\xae\xaa\xea\x06\x80\xee\xf9\xf4\xf9\xfb\xf7{2\xf5\x96%\xf9\x87\x86\x88\xac\xbd%%70Q\xf0\x11\xe7\xb0\xf5\xeb\xaf\xd7\xa2\xc5\xe2Z\x8c^\x12\x89WY\xf2r\x1a\x11G0\xa5ZE\xc6`\x91\xc2\'\x01\xd0r\xee\x07\xa4\xe5\xde\xd0\xc8\xcb\xdd\x02Z\xb6-\x80\xffc\x00\xd1\x85@,\xe6\x18\x15\x00@\xfd\x81\xf7W\x01`:qm\xc8\x12\x00\xca\x966\x10\x00\xf4\xff\x0f\xfd\xfb\xbf\x01n\xd0G\x05E\xde\xc5\xd5\x00\x00\x00\x00IEND\xaeB`\x82'

        pixbuf_loader = gtk.gdk.pixbuf_loader_new_with_mime_type( 'image/png' )
        pixbuf_loader.write( icon_blob )

        icon_pixbuf = pixbuf_loader.get_pixbuf()
        pixbuf_loader.close()

        return icon_pixbuf


if __name__ == '__main__':
    t = Terminal()
    gtk.main()

