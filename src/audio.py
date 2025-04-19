import os
from openal import (
    oalInit,
    oalGetDevice,
    oalGetContext,
    oalQuit,
    oalGetListener,
    alcOpenDevice,
    alcCreateContext,
    alcMakeContextCurrent,
    alcCloseDevice,
    alcGetCurrentContext,
    alcDestroyContext,  # Added for proper context cleanup
    oalGetDevice,  # Added for device cleanup
    alGenBuffers,
    alBufferData,
    alDeleteBuffers,
    alGenSources,
    alSourcei,
    alDeleteSources,
    alSourceStop,
    alGetSourcei,
    alGetSourcef,
    alGetSource3f,
    alSourcef,
    alSource3f,
    alSourcePause,
    alSourcePlay,
    alSourceRewind,
    AL_FORMAT_MONO8,
    AL_FORMAT_MONO16,
    AL_FORMAT_STEREO8,
    AL_FORMAT_STEREO16,
    AL_BUFFER,
    AL_LOOPING,
    AL_GAIN,
    AL_POSITION,
    AL_VELOCITY,
    AL_ORIENTATION,
    AL_SOURCE_STATE,
    AL_TRUE,
    AL_FALSE,
    AL_PLAYING,
    alGetError,
    AL_NO_ERROR,
)
import wave
import time
import numpy as np
from ctypes import c_uint, c_long, c_float, c_int, pointer

# Removed unnecessary ctypes import here


class BufferCache:
    def __init__(self, max_size=1024**2 * 512):
        self.max_size = max_size
        self.paths = []
        self.buffers = dict()
        self.current_size = 0

    def destroy_all(self):
        """Clean up all buffers and sources"""
        try:
            # Check if we have a valid OpenAL context
            if not alcGetCurrentContext():
                print("Warning: No current OpenAL context during buffer cleanup")
                return

            # Make a copy of paths since we'll be modifying it
            paths = self.paths.copy()
            for path in paths:
                source_wrapper = self.buffers.get(path)
                if source_wrapper:
                    try:
                        source_wrapper.delete()
                    except Exception as e:
                        print(f"Error deleting source for {path}: {e}")
                        # Remove from buffers even if delete fails
                        self.buffers.pop(path, None)

            # Clear remaining references
            self.paths.clear()
            self.buffers.clear()
            self.current_size = 0
        except Exception as e:
            print(f"Error during buffer cache cleanup: {e}")
            # Ensure references are cleared even if cleanup fails
            self.paths.clear()
            self.buffers.clear()
            self.current_size = 0

    def get_size(self, buffer_data):
        return len(buffer_data)

    def clean_buffers(self):
        # Remove the oldest buffers until under max_size
        while self.current_size > self.max_size and self.paths:
            old_path = self.paths.pop()
            source_wrapper = self.buffers.pop(old_path, None)
            if source_wrapper:
                source_wrapper.delete()
                print(f"Debug: Unloaded buffer for {old_path}")

    def get_buffer(self, path):
        if path not in self.buffers:
            try:
                # Check file extension and convert if needed
                if not path.lower().endswith(".wav"):
                    print(
                        f"Warning: {path} is not a WAV file. Only WAV files are supported."
                    )
                    # TODO: Add conversion from MP3/OGG to WAV using a library like pydub
                    # For now, try to find a WAV version with the same name
                    wav_path = path.rsplit(".", 1)[0] + ".wav"
                    if os.path.exists(wav_path):
                        print(f"Found WAV alternative: {wav_path}")
                        path = wav_path
                    else:
                        return None

                # Convert to absolute path if relative, but don't add extra src
                if os.path.isabs(path):
                    abs_path = path
                else:
                    # Remove 'src/' prefix if it exists
                    if path.startswith("src/"):
                        path = path[4:]
                    abs_path = os.path.abspath(os.path.join("src", path))

                if not os.path.exists(abs_path):
                    print(f"Error: File not found: {abs_path}")
                    return None

                with wave.open(abs_path, "rb") as wav_file:
                    channels = wav_file.getnchannels()
                    width = wav_file.getsampwidth()
                    rate = wav_file.getframerate()
                    frames = wav_file.readframes(wav_file.getnframes())

                    print(f"Debug: Loading WAV file: {abs_path}")
                    print(
                        f"Debug: Audio params - channels: {channels}, width: {width}, rate: {rate}, frame length: {len(frames)}"
                    )

                    # Map sample width to OpenAL format
                    if channels == 1:
                        al_format = AL_FORMAT_MONO16 if width == 2 else AL_FORMAT_MONO8
                    elif channels == 2:
                        al_format = (
                            AL_FORMAT_STEREO16 if width == 2 else AL_FORMAT_STEREO8
                        )
                    else:
                        print(f"Error: Unsupported channel count: {channels}")
                        return None

                    print(f"Debug: Using format: {al_format}")

                try:
                    # Check if OpenAL context is still current
                    current_context = alcGetCurrentContext()
                    if not current_context:
                        print("Error: OpenAL context lost before alGenBuffers!")
                        return None

                    # Create OpenAL buffer - this returns a single buffer ID

                    buf = c_uint()
                    alGenBuffers(1, pointer(buf))
                    buffer = buf.value

                    # Validate parameters before calling alBufferData
                    if not all([buffer, al_format, frames, rate]):
                        print(
                            f"Error: Invalid buffer parameters - format: {al_format}, frames length: {len(frames)}, rate: {rate}"
                        )
                        alDeleteBuffers(1, pointer(c_uint(buffer)))
                        return None

                    # Store format as c_long for OpenAL
                    al_format = c_long(al_format)

                    # Load the buffer data with all required parameters
                    try:
                        # Check context again right before buffer data
                        current_context_before_data = alcGetCurrentContext()
                        if not current_context_before_data:
                            print("Error: OpenAL context lost before alBufferData!")
                            # Fix: Pass the buffer ID directly
                            alDeleteBuffers(buffer)
                            return None

                        # Clear previous errors
                        alGetError()
                        # Convert parameters to proper types
                        size = c_int(len(frames))
                        sample_rate = c_int(rate)
                        # Ensure frames is a bytes object
                        if not isinstance(frames, bytes):
                            frames = bytes(frames)
                        alBufferData(buffer, al_format, frames, size, sample_rate)
                        # Check for errors after the call
                        error = alGetError()
                        if error != AL_NO_ERROR:
                            print(f"OpenAL Error after alBufferData: {error}")
                            # Fix: Pass the buffer ID directly
                            alDeleteBuffers(buffer)
                            return None
                    except Exception as e:
                        print(f"Python Exception during buffer data loading: {e}")
                        # Fix: Pass the buffer ID directly
                        alDeleteBuffers(buffer)
                        return None

                    # Create and configure the source
                    src = c_uint()
                    alGenSources(1, pointer(src))
                    source = src.value

                    # Set buffer using proper type
                    alSourcei(source, AL_BUFFER, c_long(buffer))

                    # Create a wrapper for the source
                    source_wrapper = Source(source, buffer)

                    # Store the source wrapper in our cache
                    self.paths.insert(0, path)
                    self.buffers[path] = source_wrapper
                    self.current_size += self.get_size(frames)
                    self.clean_buffers()
                    return source_wrapper

                except Exception as e:
                    print(f"Error creating OpenAL buffer for {abs_path}: {e}")
                    return None

            except wave.Error as e:
                print(f"Error reading WAV file {path}: {e}")
                return None
            except Exception as e:
                print(f"Error while retrieving buffer for {path}: {e}")
                return None
        return self.buffers[path]


# Custom Source wrapper class to provide the same interface as before
class Source:
    def __init__(self, source, buffer):
        self.source = int(source)  # Ensure we store the raw source ID
        self.buffer = int(buffer)  # Ensure we store the raw buffer ID

    def get_looping(self):
        try:
            looping = c_long()
            alGetSourcei(self.source, AL_LOOPING, pointer(looping))
            return looping.value == AL_TRUE
        except Exception as e:
            print(f"Error getting looping state: {e}")
            return False

    def set_looping(self, value):
        try:
            alSourcei(self.source, AL_LOOPING, AL_TRUE if value else AL_FALSE)
        except Exception as e:
            print(f"Error setting looping state: {e}")

    def get_gain(self):
        try:
            gain = c_float()
            alGetSourcef(self.source, AL_GAIN, pointer(gain))
            return gain.value
        except Exception as e:
            print(f"Error getting gain: {e}")
            return 0.0

    def set_gain(self, value):
        try:
            alSourcef(self.source, AL_GAIN, float(value))
        except Exception as e:
            print(f"Error setting gain: {e}")

    def get_position(self):
        try:
            x, y, z = c_float(), c_float(), c_float()
            alGetSource3f(self.source, AL_POSITION, pointer(x), pointer(y), pointer(z))
            return (x.value, y.value, z.value)
        except Exception as e:
            print(f"Error getting position: {e}")
            return (0.0, 0.0, 0.0)

    def set_position(self, position):
        try:
            # Ensure we have valid float values
            x, y, z = [float(v) for v in position]
            alSource3f(self.source, AL_POSITION, x, y, z)
            error = alGetError()
            if error != AL_NO_ERROR:
                print(f"Error setting source position: {error}")
            else:
                # Set default velocity for positioned sources
                alSource3f(self.source, AL_VELOCITY, 0.0, 0.0, 0.0)
        except Exception as e:
            print(f"Error configuring source 3D properties: {e}")

    def pause(self):
        try:
            alSourcePause(self.source)
        except Exception as e:
            print(f"Error pausing source: {e}")

    def play(self):
        try:
            alSourcePlay(self.source)
        except Exception as e:
            print(f"Error playing source: {e}")

    def rewind(self):
        try:
            alSourceRewind(self.source)
        except Exception as e:
            print(f"Error rewinding source: {e}")

    def get_state(self):
        try:
            state = c_long()
            alGetSourcei(self.source, AL_SOURCE_STATE, pointer(state))
            return state.value
        except Exception as e:
            print(f"Error getting source state: {e}")
            return 0

    def delete(self):
        """Clean up OpenAL resources"""
        try:
            if alcGetCurrentContext():
                # Stop playback first
                alSourceStop(self.source)

                # Delete source
                source_id = c_uint(self.source)
                alDeleteSources(1, pointer(source_id))

                # Delete buffer
                buffer_id = c_uint(self.buffer)
                alDeleteBuffers(1, pointer(buffer_id))
        except Exception as e:
            print(f"Error during Source cleanup: {e}")


class SoundManager:
    def __init__(self, buffer_cache, **kwargs):
        """Initialize the OpenAL audio system"""
        self.device = None
        self.context = None
        self.buffer_cache = buffer_cache
        self.sounds = []
        self.musics = []
        self.defaults = kwargs

        try:
            # Initialize OpenAL
            oalInit()
            alGetError()  # Clear any previous errors

            # Create new device - don't try to get existing one since oalGetDevice is not reliable
            self.device = alcOpenDevice(None)
            if not self.device:
                raise Exception("Could not open audio device")

            # Create new context - don't try to get existing one
            self.context = alcCreateContext(self.device, None)
            if not self.context:
                if self.device:
                    alcCloseDevice(self.device)
                    self.device = None
                raise Exception("Could not create audio context")

            # Make context current and verify
            alcMakeContextCurrent(self.context)
            current_context = alcGetCurrentContext()
            if not current_context:
                if self.context:
                    alcDestroyContext(self.context)
                    self.context = None
                if self.device:
                    alcCloseDevice(self.device)
                    self.device = None
                raise Exception("Could not make audio context current")

            # Clear any errors after initialization
            alGetError()

        except Exception as e:
            # Clean up any partially initialized resources
            if self.context:
                try:
                    alcMakeContextCurrent(None)
                    alcDestroyContext(self.context)
                except:
                    pass
                self.context = None
            if self.device:
                try:
                    alcCloseDevice(self.device)
                except:
                    pass
                self.device = None
            raise Exception(f"Failed to initialize audio system: {e}")

    def register_sound(self, sound):
        self.sounds.append(sound)

    def unregister_sound(self, sound):
        if sound in self.sounds:
            self.sounds.remove(sound)
            sound.destroy()

    def destroy_all(self):
        """Clean up all audio resources"""
        # Store references to context and device
        context = self.context
        device = self.device
        current_context = alcGetCurrentContext()

        try:
            # First stop all active sounds
            while self.sounds:
                try:
                    sound = self.sounds.pop()
                    sound.destroy()
                except Exception as e:
                    print(f"Error stopping sound: {e}")
            self.musics.clear()

            # Clean up buffer cache
            if hasattr(self.buffer_cache, "destroy_all"):
                try:
                    self.buffer_cache.destroy_all()
                except Exception as e:
                    print(f"Error cleaning buffer cache: {e}")

            # Clear instance variables early to prevent reuse
            self.context = None
            self.device = None

            # Then clean up OpenAL state in correct order
            if current_context:
                try:
                    # Make context not current first
                    alcMakeContextCurrent(None)
                    if context:
                        alcDestroyContext(context)
                except Exception as e:
                    print(f"Error cleaning up context: {e}")

            # Always try to close device last, even if other cleanup failed
            if device:
                try:
                    # Add a small delay to ensure context is fully released
                    time.sleep(0.1)
                    if not alcCloseDevice(device):
                        print("Error: Failed to close audio device")
                except Exception as e:
                    print(f"Error closing audio device: {e}")

            # Only quit OpenAL if we successfully cleaned up context
            if not alcGetCurrentContext():
                try:
                    oalQuit()
                except Exception as e:
                    print(f"Error during OpenAL quit: {e}")

        except Exception as e:
            print(f"Error during audio system cleanup: {e}")
            # Final emergency attempt to close device if everything else failed
            if device and device == oalGetDevice():
                try:
                    alcCloseDevice(device)
                except Exception as e:
                    print(f"Error in final device cleanup attempt: {e}")

    def play(self, path, stream=False, **kwargs):
        if not kwargs:
            kwargs = self.defaults

        source = self.buffer_cache.get_buffer(path)
        if source is None:
            return None

        sound = Sound(path, source, **kwargs)
        self.register_sound(sound)
        sound.play()
        return sound

    def stream(self, path, **kwargs):
        return self.play(path, True, **kwargs)

    def set_position(
        self, position, velocity=(0, 0, 0), orientation=(0, 0, -1, 0, 1, 0)
    ):
        """
        Set listener properties for 3D audio
        position: (x,y,z) tuple for position
        velocity: (x,y,z) tuple for velocity vector
        orientation: (at_x,at_y,at_z, up_x,up_y,up_z) tuple for orientation
        """
        try:
            listener = oalGetListener()
            if listener:
                # Clear previous errors
                alGetError()

                # Set position
                listener.set_position(position)
                error = alGetError()
                if error != AL_NO_ERROR:
                    print(f"Error setting listener position: {error}")

                # Set velocity
                listener.set_velocity(velocity)
                error = alGetError()
                if error != AL_NO_ERROR:
                    print(f"Error setting listener velocity: {error}")

                # Set orientation
                listener.set_orientation(orientation)
                error = alGetError()
                if error != AL_NO_ERROR:
                    print(f"Error setting listener orientation: {error}")
        except Exception as e:
            print(f"Error configuring 3D audio properties: {e}")

    def update(self):
        for sound in self.sounds[:]:
            if not sound.is_playing():
                self.unregister_sound(sound)


class Sound:
    def __init__(self, name, source, **kwargs):
        self.name = name
        self.source = source
        self._paused = True
        self.destroyed = False
        self.set_properties(kwargs)

    def __repr__(self):
        return self.name

    @property
    def looping(self):
        return self.source.get_looping() if not self.destroyed else False

    @looping.setter
    def looping(self, value):
        if not self.destroyed:
            self.source.set_looping(value)

    @property
    def volume(self):
        return self.source.get_gain() if not self.destroyed else -1

    @volume.setter
    def volume(self, value):
        if not self.destroyed:
            self.source.set_gain(max(0, value))

    @property
    def position(self):
        return self.source.get_position() if not self.destroyed else (0, 0, 0)

    @position.setter
    def position(self, value):
        if not self.destroyed and value:
            try:
                # Clear previous errors
                alGetError()

                # Set position
                self.source.set_position(value)
                error = alGetError()
                if error != AL_NO_ERROR:
                    print(f"Error setting source position: {error}")

                # Set default velocity if position is being tracked
                velocity = (0, 0, 0)  # Static source by default
                alSource3f(self.source, AL_VELOCITY, *velocity)
                error = alGetError()
                if error != AL_NO_ERROR:
                    print(f"Error setting source velocity: {error}")
            except Exception as e:
                print(f"Error configuring source 3D properties: {e}")

    def pause(self):
        if not self.destroyed:
            self._paused = True
            self.source.pause()

    def play(self):
        if not self.destroyed:
            self._paused = False
            self.source.rewind()  # Reset the position before playing
            self.source.play()

    def is_playing(self):
        return not self.destroyed and self.source.get_state() == AL_PLAYING

    def set_properties(self, properties):
        if not self.destroyed:
            self.volume = properties.get("gain", 1.0)
            self.looping = properties.get("looping", False)
            position = properties.get("position")
            if position:
                self.position = position

    def destroy(self):
        if not self.destroyed:
            self.pause()
            self.destroyed = True

    def restart(self):
        if not self.destroyed:
            self.source.rewind()
            self.play()
