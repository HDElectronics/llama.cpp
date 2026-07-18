/**
 * Parser for LocateAnything grounding output.
 *
 * The model emits detections as a flat stream of ref/box pairs, e.g.:
 *   <ref>MEN WALK ON MOON</ref><box><62><262><905><358></box>
 *
 * Coordinates are normalized to the 0-1000 range in `x1 y1 x2 y2` order
 * (x = horizontal, y = vertical), relative to the source image.
 */

export interface BoundingBox {
	label: string;
	/** Normalized 0-1000 coordinates. */
	x1: number;
	y1: number;
	x2: number;
	y2: number;
}

export const BOUNDING_BOX_COORD_RANGE = 1000;

// A single scan matches EITHER a label marker `<ref>label</ref>` OR a box
// `<box><x1><y1><x2><y2></box>`. The model emits one `<ref>` followed by one or
// more `<box>` entries that all share that label, e.g.:
//   <ref>sheep</ref><box><147><818><180><876></box><box><159><543><191><587></box>
// so each box inherits the most recent label. Boxes with a non-numeric payload
// (e.g. `<box>None</box>` when nothing is found) are ignored.
const TOKEN_PATTERN =
	/<ref>([\s\S]*?)<\/ref>|<box>\s*<(-?\d+)>\s*<(-?\d+)>\s*<(-?\d+)>\s*<(-?\d+)>\s*<\/box>/g;

/**
 * Extracts every detection from model output, attaching each `<box>` to the most
 * recent `<ref>` label. Returns an empty array when there is no grounding markup.
 */
export function parseBoundingBoxes(text: string | undefined | null): BoundingBox[] {
	if (!text) return [];

	const boxes: BoundingBox[] = [];
	// Reset lastIndex — the regex is stateful because of the /g flag.
	TOKEN_PATTERN.lastIndex = 0;

	let currentLabel = '';
	let match: RegExpExecArray | null;
	while ((match = TOKEN_PATTERN.exec(text)) !== null) {
		const [, label, x1, y1, x2, y2] = match;

		if (label !== undefined) {
			currentLabel = label.trim();
			continue;
		}

		boxes.push({
			label: currentLabel,
			x1: Number(x1),
			y1: Number(y1),
			x2: Number(x2),
			y2: Number(y2)
		});
	}

	return boxes;
}

/** True when the text contains at least one parseable detection. */
export function hasBoundingBoxes(text: string | undefined | null): boolean {
	return parseBoundingBoxes(text).length > 0;
}
