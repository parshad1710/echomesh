#ifndef __ECHOMESH_DEFAULTDEVICE__
#define __ECHOMESH_DEFAULTDEVICE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

const string& defaultOutputDevice();
const string& defaultInputDevice();

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_DEFAULTDEVICE__
