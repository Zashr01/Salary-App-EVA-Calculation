# Handoff: EVA Air Salary Calculator

## Overview
A salary calculation tool for EVA Air flight crew. The app calculates monthly total income based on Block Hours (with OT tiers), Per Diem (by region, with multi-step currency conversion), Base Salary, Position Allowance, and Transportation reimbursement. All values are stored in `localStorage` for persistence across sessions.

---

## About the Design Files
The file `EVA Salary Calculator.html` in this bundle is a **high-fidelity design reference built in HTML + React (Babel inline)**. It is a prototype showing the intended look, layout, interactions, and calculations — **not production code to copy directly**.

The task is to **recreate this design in your target codebase** (e.g. React, Next.js, Vue, etc.) using its established patterns, component libraries, and routing conventions. The business logic (salary formulas) should be adapted to your state management approach (Zustand, Redux, React Context, etc.).

---

## Fidelity
**High-fidelity.** Pixel-accurate colors, typography, spacing, and interactions are fully specified. Recreate the UI as closely as possible using your codebase's existing component system.

---

## Design Tokens

### Colors (EVA Air Brand)
| Token | Hex | Usage |
|---|---|---|
| `eva-green` | `#009A42` | Primary — buttons, active states, header badge, focus rings |
| `eva-green-dark` | `#007A34` | Hover state for green elements |
| `eva-green-light` | `#E6F5ED` | Green tinted backgrounds |
| `eva-green-mid` | `#CCE9D8` | Subtle green fills |
| `eva-orange` | `#EA5400` | Per diem values, OT accent, reminder banner |
| `eva-orange-light` | `#FEF0E6` | Orange tinted backgrounds |
| `bg` | `#F7F8F6` | Page background |
| `surface` | `#FFFFFF` | Card / sidebar background |
| `border` | `#E4E8E2` | Default border |
| `border-strong` | `#CBD2C7` | Stronger border / scrollbar |
| `text` | `#111810` | Primary text |
| `text-mid` | `#4A5248` | Secondary text |
| `text-muted` | `#8A9488` | Labels, captions |
| `text-faint` | `#B8BDB6` | Disabled / placeholder |
| `purple` | `#6B7CFF` | Fixed/Salary category accent |
| `red` | `#E02020` | Super OT tier |

### Typography
| Role | Font | Size | Weight | Notes |
|---|---|---|---|---|
| App name / headings | Plus Jakarta Sans | 14–32px | 700–800 | Letter spacing -0.025em to -0.04em |
| Body / labels | Inter | 11–14px | 400–600 | Label: 11px, 0.055em spacing, uppercase |
| Numbers / mono | JetBrains Mono | 12–28px | 500–700 | All financial figures |

### Spacing & Radius
| Token | Value |
|---|---|
| `radius-sm` | 8px |
| `radius` | 12px |
| `radius-lg` | 16px |
| Sidebar width | 304px |
| Header height | 56px |
| Card padding | 18–20px |
| Section head padding | 16px 20px |

### Shadows
```
shadow-sm:  0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)
shadow:     0 4px 16px rgba(0,0,0,0.07), 0 1px 4px rgba(0,0,0,0.04)
shadow-lg:  0 12px 40px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06)
green-glow: 0 4px 20px rgba(0,154,66,0.3)
orange-glow: 0 4px 16px rgba(234,84,0,0.2)
```

---

## Layout & Structure

```
<App>
  ├── <Sidebar>          // Slide-in drawer, 304px, left edge
  ├── <Header>           // Sticky, 56px height
  └── <Main>             // Max-width 840px, centered, px-16
       ├── [Inputs Tab]
       │    ├── <BlockHoursCard>
       │    ├── <PerDiemCard>
       │    ├── <SalaryCard>
       │    └── <ViewResultsButton>
       └── [Results Tab]
            ├── <TopMetrics>         // 3 cards, 2fr 1fr 1fr grid
            ├── <DistributionBar>
            ├── <BreakdownTables>    // 3 category sections
            ├── <GrandTotalBanner>
            ├── <ThaiReminderBanner>
            └── <BackButton>
```

---

## Screens / Views

### Header (Sticky, always visible)
- Height: 56px, `background: rgba(247,248,246,0.92)`, `backdrop-filter: blur(12px)`, bottom border `#E4E8E2`
- **Hamburger button** (left): opens Sidebar. 18px icon, hover bg `#E6F5ED`
- **Logo** (left): 28×28px rounded-7 green square with white plane icon + "EVA **Salary**" text (bold, green word)
- **Profile name input** (inline, editable): transparent input, 13px Inter 500, `color: text-muted`. Saves to state.
- **Tab toggle** (center-right): Inputs (green when active) / Results (orange when active). Background `#F7F8F6`, border `#E4E8E2`, padding 3px, gap 2px. Active tab: colored bg + white text, box-shadow `0 1px 4px rgba(0,0,0,0.1)`.
- **Total pill** (right): `background: #009A42`, border-radius 9px, padding `6px 14px`. Label 10px "TOTAL" at 70% white opacity. Value in JetBrains Mono 14px white bold.

---

### Sidebar (Configuration)
- **Overlay**: `rgba(0,0,0,0.25)` with `backdrop-filter: blur(2px)`, closes on click
- **Drawer**: 304px, white bg, slides in from left, box-shadow lg
- **Header row**: bg `#F7F8F6`, green cog icon + "Configuration" title, ✕ close button
- **Tab bar**: 4 tabs (Rates / Per Diem / Exchange / Transport). Underline style — active tab has `border-bottom: 2px solid #009A42`, green text. Inactive: muted text, transparent border.
- **Content area**: padding 20px 18px, gap 16px between fields

#### Rates Tab
- Exchange Rate input (suffix ×)
- Divider
- Normal Rate (0–70h) suffix ฿/h
- OT Rate (71–80h) suffix ฿/h
- Super OT Rate (>80h) suffix ฿/h
- Rate summary box: `bg: #F7F8F6`, radius 8, 3 rows with range label (left) + green mono value (right)

#### Per Diem Tab
- EUR/AME/AUS Multiplier (suffix ×)
- Other Regions Multiplier (suffix ×)
- Divider
- "Withdraw As" toggle: USD / TWD — 2-column grid buttons. Active: green bg + white text. Inactive: bg-bg + border.
- If TWD selected: show Cathay Rate input

#### Exchange Tab
- Info box: `bg: #E6F5ED`, green text, explains SuperRich rate
- SuperRich Rate input (USD→THB if USD selected, TWD→THB if TWD)

#### Transport Tab
- Rate per Trip input (suffix ฿)

---

### Input: Block Hours Card
- **Section header**: green clock icon in 30×30 green-light rounded square. Title "Block Hours", sub = computed total hrs
- **Body**: padding 18px 20px, gap 16px

**HH:MM Input row**: Two adjacent inputs (Hours | Minutes), each with suffix h/m. Right-aligned sublabel shows computed income in green mono.

**Tier distribution bar**: flex row, height 6px, gap 2px, 3 segments (flex proportional to max hrs):
- Green segment (flex 70) — Normal
- Orange segment (flex 10) — OT
- Red segment (flex 20) — Super OT
Each fills to `(actual_hrs / max_hrs) * 100%` via inner div with transition `width 0.35s ease`

**Tier cards grid** (3 columns, gap 8):
- Normal: bg `#E6F5ED`, border `#009A4222`, label "NORMAL 0–70h" green, hrs in mono 14px, income in green mono 12px
- OT: bg `#FEF0E6`, orange, "OT 71–80h"
- Super OT: bg `#FFF0F0`, red `#E02020`, ">80h"

---

### Input: Per Diem Card
- **Section header**: globe icon, "Per Diem Hours", sub "Hours flown by region type"
- Two HH:MM inputs (EUR/AME/AUS; Other Regions) with sublabels showing `×multiplier = X.XX USD`
- Divider between them
- 2-col summary row at bottom:
  - "Per Diem Base" → orange mono value (USD)
  - "After Exchange" → green mono value (฿)
  - Both: bg `#F7F8F6`, border `#E4E8E2`, radius 8, padding 12px 14px

---

### Input: Salary & Allowances Card
- **Section header**: dollar icon, "Salary & Allowances"
- 2-col grid: Base Salary | Position Allowance (both suffix ฿, step 100)
- Divider
- 2fr 1fr grid: Transport Rate / Trip | Trips (suffix ×, step 1, min 0)
- Transport total row: flex space-between, bg `#F7F8F6`, border, padding 10px 14px. Label left (muted), value right (mono bold)

---

### Results: Top Metrics (3 cards, `2fr 1fr 1fr`)
**Grand Total card** (2fr):
- bg `#009A42`, radius 16, padding 22px 24px, box-shadow green-glow
- Label: 11px uppercase, `rgba(255,255,255,0.65)`, letter-spacing 0.07em
- Value: Plus Jakarta Sans 800, 32px, white, line-height 1
- Sub: 12px, `rgba(255,255,255,0.55)`

**Per Diem / Withdrawal cards** (1fr each):
- White bg, border, radius 16, shadow-sm
- Label: 11px uppercase muted
- Value: Plus Jakarta Sans 800, 20px
- Sub: 11px faint, JetBrains Mono

---

### Results: Distribution Bar
- White card, padding 16px 20px 18px
- Title: Plus Jakarta Sans 700, 13px
- Bar: flex, height 8px, radius 4, overflow hidden, gap 2px
  - Segments: Green (Block Hours), Orange (Per Diem), Purple `#6B7CFF` (Salary), Faint (Transport)
  - `flex: value` — proportion auto-adjusts via CSS flex
- Legend grid (4 cols): 8×8 rounded-2 color dot + label (10px uppercase) + value (mono 13px bold) + pct (11px faint)

---

### Results: Breakdown Tables (3 sections)
One card per category. Each has:
- **Category header row**: 3px wide × 14px tall colored pill + uppercase label (11px, 0.07em spacing)
- **Data rows** (alternating subtle bg on even rows: `rgba(0,0,0,0.012)`):
  - Left: label (13px 500) + detail (11px faint mono below)
  - Right: amount (mono 14px bold, orange if non-THB) + currency tag (10px faint, below)

Categories:
1. Block Hours — green pill, 3 rows (Normal / OT / Super OT)
2. Per Diem — orange pill, 3 rows (Base USD / Withdrawal / Exchange THB)
3. Fixed & Allowances — purple `#6B7CFF` pill, 3 rows (Base / Position / Transport)

---

### Results: Grand Total Banner
- bg `#009A42`, radius 16, padding 20px 24px, flex space-between
- Left: "Grand Total" (Plus Jakarta Sans 800, 16px, white) + profile name (12px, 55% white)
- Right: value (JetBrains Mono 700, 28px, white) + "Thai Baht" (11px, 50% white)

---

### Results: Thai Reminder Banner
- bg `#FEF0E6`, border `rgba(234,84,0,0.18)`, radius 12, padding 14px 18px
- Flex row, gap 12, align items center
- 💸 emoji (22px, flex-shrink 0)
- Text: `"เงินเยอะจังหายไปไหนนะ อย่าลืมวางแผนการเงินนะจร๊ะ"` — 13.5px, fontWeight 600, color `#EA5400`, line-height 1.6

---

## Inputs (NumInput Component)
All number inputs share this style:
- bg: white
- border: `1.5px solid #E4E8E2` (default) → `1.5px solid #009A42` (focused)
- border-radius: 8px
- padding: 9px 12px (right 36px if suffix)
- font: JetBrains Mono 500, 14px
- focus ring: `box-shadow: 0 0 0 3px rgba(0,154,66,0.1)`
- shadow-sm always applied

Label: 11px Inter 600, uppercase, letter-spacing 0.055em, color `text-muted`

---

## Business Logic (Salary Calculations)

```js
// Block Hours
const total_bh = bh_hours + bh_mins / 60;
const bh_normal = Math.min(total_bh, 70);
const bh_ot     = Math.max(Math.min(total_bh - 70, 10), 0);
const bh_sot    = Math.max(total_bh - 80, 0);
const inc_normal = bh_normal * normal_rate;
const inc_ot     = bh_ot * ot_rate;
const inc_sot    = bh_sot * super_ot_rate;
const total_bh_income = inc_normal + inc_ot + inc_sot;

// Per Diem
const p1_total = p1_hours + p1_mins / 60;
const p2_total = p2_hours + p2_mins / 60;
const pd_usd = (per_diem_euro_mult * p1_total) + (per_diem_other_mult * p2_total);

// Currency conversion
const hold_amt = withdrawal_currency === 'TWD' ? pd_usd * cathay_rate : pd_usd;
const sr_rate  = withdrawal_currency === 'USD'  ? superrich_rate_usd : superrich_rate_twd;
const pd_thb   = hold_amt * sr_rate;

// Totals
const transport_income = transport_trips * transport_rate;
const grand_total = total_bh_income + pd_thb + base_salary + position_allowance + transport_income;
```

---

## Default Values
```js
{
  exchange_rate: 1.0,
  normal_rate: 120.0,
  ot_rate: 300.0,
  super_ot_rate: 420.0,
  per_diem_euro_mult: 4.0,
  per_diem_other_mult: 3.5,
  withdrawal_currency: "USD",
  cathay_rate: 31.6,
  superrich_rate_usd: 34.0,
  superrich_rate_twd: 1.05,
  transport_rate: 700.0,
  bh_hours: 89, bh_mins: 38,
  p1_hours: 175, p1_mins: 43,
  p2_hours: 158, p2_mins: 37,
  base_salary: 16000.0,
  position_allowance: 1000.0,
  transport_trips: 6,
  profile_name: "My Profile"
}
```

---

## State Management
All state is flat key-value. Persisted to `localStorage` (keys: `eva_vals2`, `eva_tweaks2`). Two categories:

**Input values** (`eva_vals2`): All numeric/string inputs above  
**Tweaks** (`eva_tweaks2`): `{ showBreakdown: true, compactMode: false }`

No server-side state required for the core app. The original Python app (Streamlit) supported Google Sheets sync for multi-device profiles — if needed, add an API layer with profile ID + device cookie logic.

---

## Interactions & Behavior

| Interaction | Behavior |
|---|---|
| Hamburger → sidebar opens | Slide in from left (transform translateX), overlay fades in |
| Click overlay | Sidebar closes |
| Sidebar config tabs | Underline indicator, content swaps in-place |
| USD/TWD toggle | Conditional Cathay Rate field appears |
| All number inputs | Recalculate instantly on change |
| "View Results" button | Switch to Results tab |
| "Back to Inputs" button | Switch to Inputs tab |
| Profile name (header) | Inline editable text input |
| Results tab | Grand total hero card, distribution bar, breakdown, grand total banner, Thai reminder |

### Transitions
- Sidebar slide: `transform 0.26s cubic-bezier(0.4,0,0.2,1)`
- Overlay fade: `opacity 0.2s`
- Tier bars fill: `width 0.35s ease`
- Distribution segments: `flex 0.5s ease`
- Input focus: `border-color 0.15s`

---

## Assets
- **Fonts**: Plus Jakarta Sans, Inter, JetBrains Mono — all from Google Fonts
- **Icons**: Hand-drawn inline SVG paths (no external icon library). See source HTML for all SVG path data.
- **Plane icon**: SVG fill path (no stroke)

---

## Files in This Bundle

| File | Description |
|---|---|
| `EVA Salary Calculator.html` | Full hi-fi prototype — single file React app with all logic |
| `README.md` | This document |

---

## Notes for Developer
- The original app was built in **Python + Streamlit** with Google Sheets as a backend DB. The redesign is frontend-only. If you need multi-device persistence, implement a simple REST/Firebase/Supabase backend and replace `localStorage` calls.
- The Tweaks panel (bottom-right floating) is a design tool only — it can be removed in production or repurposed as a settings panel.
- Ensure Thai Unicode renders correctly (`เงินเยอะจัง...`) — use UTF-8 charset and a font that includes Thai glyphs (Inter supports Thai).
