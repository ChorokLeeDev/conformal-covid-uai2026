# Poster Design Notes

Use this checklist for every future edit to `poster.tex`. These are the design constraints that were repeatedly emphasized during poster iteration.

## Non-Negotiable Visual Checks

- Always rebuild the PDF after poster edits.
- Always render the PDF to an image and visually inspect it before reporting back.
- Always check the bottom/footer area specifically: no overlap between content, logos, footer graphics, or page boundary. This check is mandatory even for edits that seem unrelated to the footer, because column height changes can create new overlap.
- When checking the render, inspect both the full poster and the specific edited region.
- Always open the final PDF after changes when the poster itself was edited.
- Keep the poster to one A0 portrait page: 33.1 in x 46.8 in / 84.1 cm x 118.9 cm.

## Overall Layout

- The middle column should be the visual focus and may be wider than the side columns.
- The main result block should feel dominant, not cramped or secondary.
- Left and right columns can be narrower if that helps the center become more prominent.
- Avoid adding content that pushes the center column into the footer area.
- Blocks need balanced internal padding: not just top padding, also bottom padding.
- Avoid awkward empty space above or below blocks.
- Keep the layout professional, clean, and conference-poster-like rather than decorative.

## Footer And Logos

- Current footer decision: do not use a footer delimiter. It caused repeated overlap with the center column and should stay removed unless the whole footer is redesigned.
- Do not use a footer delimiter if it risks crossing or touching any content block.
- If a delimiter is used later, it must be visually checked against the rendered poster, not assumed safe from coordinates.
- KAIST and SAP logos should sit in the footer without touching poster content.
- KAIST should be independently positioned and centered in the left footer half; SAP should be independently positioned and centered in the right footer half. Do not group them in one tabular/footer row.
- Align logos visually, not by LaTeX box geometry. The logo files have different internal whitespace.
- SAP should not appear higher than KAIST.
- SAP has large internal whitespace in the source image; crop it in LaTeX before judging size or alignment.
- Logos should be large enough to read clearly, but must not crowd the poster body or page edge.

## Typography And Spacing

- Avoid glued words and strange spacing in headings, captions, and takeaway boxes.
- Avoid excessive word spacing caused by forced justification or manual spacing.
- Headlines should be prominent but not cartoonishly large.
- Keep font sizes consistent within comparable block types.
- Captions and explanatory text must be readable at poster scale.
- Important statistical text should not be tiny, especially p-values and headline metrics.
- Do not let text touch box borders; maintain clear internal padding.
- For framed text callouts, use explicit internal padding rather than relying on the default `\fboxsep`.
- The `Research Question` callout must have visible padding between the text and border. The text should not read like `CanwepredictwhenCPfailsbefore deployment?` or touch the border.
- Keep a clear gap between `Research Question:` and the following framed box.
- Do not leave line breaks that make key phrases look broken or unnatural.

## Color And Style

- Keep the poster blue-dominant and restrained.
- Avoid too many competing colors.
- Orange should be used sparingly for emphasis, not as a general section color.
- `Why Not Standard Shift Tests?` should stay blue, not orange.
- Avoid overly busy visual effects.

## Headline And Takeaway

- The top summary/headline must be aesthetically polished and readable.
- The main takeaway should be prominent and centered.
- The three headline metric boxes should be centered and evenly spaced.
- Do not make the main metric row too tall or vertically stretched.
- The main result should clearly communicate: higher SHAP concentration tracks larger CP coverage loss.
- Avoid unexplained shorthand in the headline. If using LOO-CV or similar terms, define or avoid them.

## Figures And Captions

- Only the two middle-column scientific figures should be numbered.
- The main correlation plot should be `Fig. 1`.
- The mechanism figure should be `Fig. 2`.
- Remove the left-column timeline caption; it should not be numbered as a scientific figure.
- Figure captions must explain what the viewer is seeing and why it matters.
- Figures need immediate interpretation, not just a label.
- Fig. 1 should explain that each point is a task, x-axis is pre-deployment concentration, and y-axis is coverage drop.
- Fig. 2 should explain the four panels and the mechanism: concentrated reliance can create a single point of failure.
- Avoid large gaps between a figure title/caption line and the next explanatory line.

## Content Hierarchy

- Main Result belongs in the center.
- Mechanism and theorem belong near the center, not buried.
- Short model scope belongs near the main result if needed; detailed scope belongs lower, not in the right-column main flow.
- `Why Not Standard Shift Tests?` can live in the left column near motivation/data.
- `Paper, Code & Contact` works best at the right-bottom position with the QR code visible.
- Avoid redundant tables if they do not add immediate value, such as the old `Analysis Set / Count` table.
- Keep the contact email synchronized across poster and presentation script: `choroklee@kaist.ac.kr`.

## Wording Preferences

- Use `%`, never `\%`, in visible poster text.
- Avoid labels that are unclear without explanation, such as unexplained `accuracy` or `LOO-CV accuracy`.
- Be precise about what accuracy means if it appears.
- Prefer unified evaluation language across checks, such as `11/12 rule labels matched` rather than mixing SALT-only and total counts.
- Do not overstate results. Clarify when a cutoff is exploratory.
- For specificity checks, explain that low-concentration checks are negative controls and define coverage drop in pp.

## Theory Section

- The theorem needs its own explanation, not only a formula.
- Explain the implication in plain language: if the dominant shifted feature weakens true-class support, larger concentration puts more weight on the damaged signal, APS scores rise, and coverage drops.
- Leave enough vertical space between the theorem formula and its interpretation.
- Keep the math readable, but do not let it overwhelm the empirical story.

## Scope And Future Work

- Be clear that the headline finding is for GBM/LightGBM multiclass APS conformal predictors.
- Explain that RF and MLP can fail differently; do not leave this as a vague one-line contrast.
- Mention neural diagnostics / gradient-based explanations as future work for MLPs.
- Mention prospective validation and possible top-n expansion when relevant.
- Open questions should use available space, but not crowd the right column.

## Presentation Script Sync

- Keep `poster/presentation_english.md` synchronized with the current poster after content or structure changes.
- The English script should use current figure numbering only: `Fig. 1` for the correlation plot and `Fig. 2` for the mechanism figure.
- Remove stale references immediately: no `Fig. 3`, no `LOO-CV accuracy`, no `87.5%` if it is not on the poster, and no old email address.
- The script should describe the current block order: left motivation/shift-test contrast, center main result and mechanism/theory, right specificity/scope/future work/contact.
- Include a short poster-flow version with pointing cues for live presentation.
- Use the same statistical wording as the poster: `ρ = 0.853`, `p < 0.001`, `n = 16`, `9 domains`, `91.7%`, and `11/12 rule labels matched`.
