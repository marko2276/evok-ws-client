import setuptools

setuptools.setup(
        name='evok-ws-client',
        version='0.0.1',
        description='Client for connectin to Unipi devices runing EVOK API via websockets',
        author="Marko Vaupotic",
        url='https://github.com/marko2276/evok-ws-client',
        license='MIT',
        packages=setuptools.find_packages(),
        keywords = ['evok', 'unipi', 'websockets', 'home-assistant'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
        ],
        install_requires=['websockets'],
        python_requires='>=3',
)
