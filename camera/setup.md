Raspberry Pi 4B (8Gb)
element14 Raspberry Pi CSI Camera NOIR
USB-C Power cable
Heatsinks
Fan
Case
SD-Card

flash Ubuntu 20.10 arm64-raspi to SD Card with rpi-imager
connect hdmi, usb c power, fan, camera, mouse, keyboard
boot by powering usb
graphical system setup (future version with headless ubuntu server)
location settings
user name:pi , password:farmrobot
connecting wifi/ethernet
sudo apt update && sudo apt upgrade
sudo nano /boot/firmware/config.txt [gpu_mem=512 ; start_x=1]

using v4l2m2m encoder to have arm64 hardware support to efficiently encode a efficient h.265 stream which is sent via rtmp to a server which reencodes to hls to view video stream in a browser
v4l2m2m:
https://www.willusher.io/general/2020/11/15/hw-accel-encoding-rpi4
build latest ffmpeg from source to enable needed packages / encoders
Following guide: https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
cd /home/pi/
mkdir -p ~/ffmpeg_sources ~/ffmpeg_build
mkdir -p ~/bin (installing to /home/pi/bin/ to avoid conflicts with the system package manager)
installing dependencies:
sudo apt-get update -qq && sudo apt-get -y install \
  autoconf \
  automake \
  build-essential \
  cmake \
  git-core \
  libass-dev \
  libfreetype6-dev \
  libgnutls28-dev \
  libgnutls-dev \
  libsdl2-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  meson \
  ninja-build \
  pkg-config \
  texinfo \
  wget \
  yasm \
  zlib1g-dev \
  libunistring-dev

installing libaries, chosing wich are needed:

NASM (An assembler used by some libraries.)
cd ~/ffmpeg_sources && \
wget https://www.nasm.us/pub/nasm/releasebuilds/2.15.05/nasm-2.15.05.tar.bz2 && \
tar xjvf nasm-2.15.05.tar.bz2 && \
cd nasm-2.15.05 && \
./autogen.sh && \
PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" && \
make -j 4 && \
make install

libx264 (H.264 video encoder, fallback)
cd ~/ffmpeg_sources && \
git -C x264 pull 2> /dev/null || git clone --depth 1 https://code.videolan.org/videolan/x264.git && \
cd x264 && \
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --enable-static --enable-pic && \
PATH="$HOME/bin:$PATH" make -j 4 && \
make install

libx265 (H.265/HEVC video encoder)
sudo apt-get install libnuma-dev && \
cd ~/ffmpeg_sources && \
git -C x265_git pull 2> /dev/null || git clone https://bitbucket.org/multicoreware/x265_git && \
cd x265_git/build/linux && \
PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED=off ../../source && \
PATH="$HOME/bin:$PATH" make -j 4 && \
make install

libvpx (VP8/VP9 video encoder/decoder, another efficient video encoder, needs testing)
cd ~/ffmpeg_sources && \
git -C libvpx pull 2> /dev/null || git clone --depth 1 https://chromium.googlesource.com/webm/libvpx.git && \
cd libvpx && \
PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm && \
PATH="$HOME/bin:$PATH" make -j 4 && \
make install

libaom (AV1 video encoder/decoder)
cd ~/ffmpeg_sources && \
git -C aom pull 2> /dev/null || git clone --depth 1 https://aomedia.googlesource.com/aom && \
mkdir -p aom_build && \
cd aom_build && \
PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED=off -DENABLE_NASM=on ../aom && \
PATH="$HOME/bin:$PATH" make -j 4 && \
make install

libsvtav (AV1 video encoder/decoder)
cd ~/ffmpeg_sources && \
git -C SVT-AV1 pull 2> /dev/null || git clone https://gitlab.com/AOMediaCodec/SVT-AV1.git && \
mkdir -p SVT-AV1/build && \
cd SVT-AV1/build && \
PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DCMAKE_BUILD_TYPE=Release -DBUILD_DEC=OFF -DBUILD_SHARED_LIBS=OFF .. && \
PATH="$HOME/bin:$PATH" make -j 4 && \
make install

libdav1d (AV1 decoder, much faster than the one provided by libaom
Users whose distributions don't provide a recent enough version of meson (0.49.0 or newer) will need to install a more up-to-date version. This is easily done via the Python Package Index:
sudo apt-get install python3-pip && \
pip3 install --user meson

cd ~/ffmpeg_sources && \
git -C dav1d pull 2> /dev/null || git clone --depth 1 https://code.videolan.org/videolan/dav1d.git && \
mkdir -p dav1d/build && \
cd dav1d/build && \
meson setup -Denable_tools=false -Denable_tests=false --default-library=static .. --prefix "$HOME/ffmpeg_build" --bindir="$HOME/bin" --libdir="$HOME/ffmpeg_build/lib" && \
ninja && \
ninja install

Audio libaries are probably needed for building, especially libfdk_aac for vpx
libfdk-aac (AAC audio encoder)
cd ~/ffmpeg_sources && \
git -C fdk-aac pull 2> /dev/null || git clone --depth 1 https://github.com/mstorsjo/fdk-aac && \
cd fdk-aac && \
autoreconf -fiv && \
./configure --prefix="$HOME/ffmpeg_build" --disable-shared && \
make -j 4 && \
make install

libmp3lame
libopus

Building FFmpeg
cd ~/ffmpeg_sources && \
wget -O ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2 && \
tar xjvf ffmpeg-snapshot.tar.bz2 && \
cd ffmpeg && \
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$HOME/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$HOME/ffmpeg_build/include" \
  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --bindir="$HOME/bin" \
  --enable-gpl \
  --arch=aarch64 \
  --enable-gnutls \
  --enable-libaom \
  --enable-libsvtav1 \
  --enable-libdav1d \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-nonfree && \
PATH="$HOME/bin:$PATH" make -j 4 && \
make install && \
hash -r
    
source ~/.profile

sudo apt install v4l-utils

sudo apt install openssh-server
sudo ufw allow ssh
ssh pi@farmrobot
