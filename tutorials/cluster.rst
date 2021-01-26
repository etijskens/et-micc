standard python distribution from python.org
Python versions available on Leibniz on Jan 2021:
Python/2.7.13-intel-2017a
Python/2.7.14-intel-2018a
Python/2.7.15-intel-2018b
Python/2.7.16-intel-2019b
Python/3.6.1-intel-2017a
Python/3.6.4-intel-2018a
Python/3.6.6-intel-2018a
Python/3.6.8-intel-2018b
Python/3.7.0-intel-2018b
Python/3.7.1-intel-2018b
Python/3.7.4-intel-2019b
Python/3.8.3-intel-2020a

Intel Python distribution
IntelPython2/2019b -> Python 2.7.16
IntelPython3/2019b IntelPython3-Packages/2019b IntelPython3-Packages/2019b-GCCcore-8.3.0 -> Python 3.6.9
IntelPython3/2020a IntelPython3-Packages/2020a-intel-2020a -> Python 3.7.7

> module load git
> module load IntelPython3/2020a
> module load IntelPython3-Packages/2020a
> python -m venv .venv --system-site-packages
> pip install numpy
Requirement already satisfied: numpy in /apps/antwerpen/x86_64/centos7/intel-psxe/2020.02/intelpython3/lib/python3.7/site-packages (1.18.5)