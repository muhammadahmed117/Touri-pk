import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Setup Figure
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')

# Function to draw a Persona Card
def draw_card(x, y, name, role, bio, keywords, color, icon_color):
    # Main Card Background (Shadow first for depth)
    shadow = patches.FancyBboxPatch((x+0.1, y-0.1), 5, 6, boxstyle="round,pad=0.1", fc='#ccc', ec='none', zorder=1)
    ax.add_patch(shadow)
    card = patches.FancyBboxPatch((x, y), 5, 6, boxstyle="round,pad=0.1", fc='white', ec='#ddd', linewidth=1, zorder=2)
    ax.add_patch(card)
    
    # Header Color Block
    header = patches.FancyBboxPatch((x, y+4.5), 5, 1.5, boxstyle="round,pad=0.1", fc=color, ec='none', zorder=3)
    ax.add_patch(header)
    # Fix bottom corners of header to be square (visual trick)
    rect_fix = patches.Rectangle((x, y+4.5), 5.2, 0.5, fc=color, ec='none', zorder=3) 
    # (Simplified: just letting the rounded top header stay)

    # "Profile Picture" Placeholder
    circle = patches.Circle((x+2.6, y+4.5), 0.9, fc='white', ec=icon_color, linewidth=3, zorder=4)
    ax.add_patch(circle)
    plt.text(x+2.6, y+4.5, name[0], ha='center', va='center', fontsize=30, fontweight='bold', color=icon_color, zorder=5)

    # Text Content
    # Name & Role
    plt.text(x+2.6, y+3.2, name, ha='center', va='center', fontsize=16, fontweight='bold', color='#333', zorder=5)
    plt.text(x+2.6, y+2.8, role, ha='center', va='center', fontsize=11, style='italic', color='#666', zorder=5)
    
    # Bio
    plt.text(x+2.6, y+1.8, bio, ha='center', va='center', fontsize=10, color='#444', wrap=True, zorder=5)

    # Keywords (Tags)
    tag_y = y + 0.8
    plt.text(x+2.6, tag_y, f"TRAITS:\n{keywords}", ha='center', va='center', fontsize=9, fontweight='bold', color=icon_color, zorder=5)

# --- Data from Source 55 & 56 ---

# Card 1: Saira
bio_saira = "A busy young professional in Singapore.\nShe values health and convenience.\nWants organic options but lacks time to cook."
draw_card(0.5, 0.5, "Imran", "The Professional", bio_saira, 
          "• Health-Conscious\n• Willing to pay for Time\n• Seeks Convenience", "#81c784", "#2e7d32")

# Card 2: Rizwan
bio_rizwan = "An Expat living in Singapore.\nHe misses Western comfort foods.\nAdventurous eater seeking global flavors."
draw_card(6.5, 0.5, "RIZWAN", "The Expat / Explorer", bio_rizwan, 
          "• Global Palate\n• Seeks 'Taste of Home'\n• Values Novelty", "#64b5f6", "#1565c0")

plt.title("Target Customer Personas", fontsize=18, fontweight='bold', color='#333', y=0.95)
plt.tight_layout()
plt.savefig('persona_cards.png', dpi=300)
plt.show()