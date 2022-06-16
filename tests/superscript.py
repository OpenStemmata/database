# normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
# super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
normal = "0123456789ae"
super_s = "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵉ"
sub_s = "₀₁₂₃₄₅₆₇₈₉ₐₑ"

def get_super(x):
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)

def get_sub(x):
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)

def get_normal(x):
    res = x.maketrans(''.join(super_s + sub_s), ''.join(normal + normal))
    return x.translate(res)


