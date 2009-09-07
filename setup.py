import glob
from distutils.core import setup
from distutils.command.install_data import install_data

class smart_install_data(install_data):
  def run(self):
    #need to change self.install_dir to the library dir
    install_cmd = self.get_finalized_command('install')
    self.install_dir = getattr(install_cmd, 'install_lib')
    return install_data.run(self)

setup (name='pinna',
  version='4.5b',
  description='Pinna is an awesome MPD frontend written in python using GTK for the GUI',
  author='m0nk',
  author_email='monkapotomus90@gmail.com',
  url='http://m0nk.hopto.org/',
  license='GPL',
  packages=['pinna'],
  scripts=['scripts/pinna'],
  cmdclass = {'install_data':smart_install_data},
  data_files=[('pinna/glade',glob.glob('pinna/glade/*.glade')),('pinna/glade',glob.glob('pinna/glade/*.png')),('/usr/share/applications',['pinna.desktop']),
  ('/usr/share/pixmaps',['pinna.xpm'])]
  )
