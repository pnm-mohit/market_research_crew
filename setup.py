from setuptools import setup, find_packages

setup(
    name='market_research_crew',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'crewai>=0.28.0',
        'langchain>=0.0.267',
        'flask>=2.0.0',
        'flask-socketio>=5.3.0',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
        'pyyaml>=6.0',
        'textblob',
        'yfinance',
        'pandas',
        'numpy',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'market-research=market_research_crew.web.app:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='AI-Powered Market Research Crew',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/market_research_crew',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
) 