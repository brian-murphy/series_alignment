from setuptools import setup

setup(name='series_alignment',
      version='0.0.2',
      description='Tool for aligning two series visually',
      url='http://github.com/brian-murphy/series_alignment',
      author='Brian Murphy',
      author_email='brianmurphy@gatech.edu',
      license='MIT',
      packages=['series_alignment'],
      zip_safe=False,
      entry_points= {
          'console_scripts': ["series_alignment=series_alignment.command_line:main"]
      })
