#ifndef __ECHOMESH_COLORS__
#define __ECHOMESH_COLORS__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

struct FColor {
  FColor() {}
  FColor(float red, float green, float blue, float alpha=1.0)
      : red_(red), green_(green), blue_(blue), alpha_(alpha) {
  }
  FColor(const Colour& c)
      : red_(c.getFloatRed()),
        green_(c.getFloatGreen()),
        blue_(c.getFloatBlue()),
        alpha_(c.getFloatAlpha()) {
  }

  float alpha() const { return alpha_; }

  float red() const { return red_; }
  float green() const { return green_; }
  float blue() const { return blue_; }

  float hue() const { return red_; }
  float saturation() const { return green_; }
  float brightness() const { return blue_; }

  operator Colour() const {
    return Colour::fromFloatRGBA(red_, green_, blue_, alpha_);
  }

  bool operator==(const FColor& other) const;

  void scale(float f) {
    red_ *= f;
    green_ *= f;
    blue_ *= f;
  }

  static FColor NO_COLOR;

  void combine(const FColor& other) {
    red_ = std::max(red_, other.red_);
    green_ = std::max(green_, other.green_);
    blue_ = std::max(blue_, other.blue_);
    alpha_ = std::max(alpha_, other.alpha_);
  }

  FColor toHSB() const;
  FColor fromHSB() const;
  FColor toYIQ() const;
  FColor fromYIQ() const;

 private:
  float red_, green_, blue_, alpha_;
};

typedef vector<FColor> FColorList;

bool fillColor(const String& name, FColor* color);
FColor colorFromInt(uint32 argb);
string colorName(const FColor& color);
inline void copyColor(const FColor& from, FColor* to) { *to = from; }
void sortFColorList(FColorList*);
int compareColors(const FColor& x, const FColor& y);
int countColorsInList(const FColorList&, const FColor&);
int indexColorInList(const FColorList&, const FColor&);
void reverseFColorList(FColorList*);
void fillFColorList(
    FColorList*, const FColor& begin, const FColor& end, int size);

FColor interpolate(const FColor& begin, const FColor& end, float ratio);

inline FColor makeFColor(float red, float green, float blue, float alpha) {
  return FColor(red, green, blue, alpha);
}

inline void scaleFColorList(FColorList* fc, float scale) {
  for (auto& c: *fc)
    c.scale(scale);
}

inline void combineFColorList(const FColorList& from, FColorList* to) {
  if (from.size() > to->size())
    to->resize(from.size());
  for (auto i = 0; i < from.size(); ++i)
    (*to)[i].combine(from[i]);
}

}  // namespace echomesh

#endif  // __ECHOMESH_COLORS__
