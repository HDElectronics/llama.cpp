<script lang="ts">
	import { BOUNDING_BOX_COORD_RANGE, type BoundingBox } from '$lib/utils';

	interface Props {
		/** Source image the boxes are drawn on (base64 data URL). */
		imageSrc: string;
		boxes: BoundingBox[];
		alt?: string;
	}

	let { imageSrc, boxes, alt = 'Detected objects' }: Props = $props();

	// Distinct, high-contrast hues cycled per detection.
	const COLORS = [
		'#ef4444',
		'#3b82f6',
		'#22c55e',
		'#f59e0b',
		'#a855f7',
		'#ec4899',
		'#14b8a6',
		'#eab308'
	];

	const R = BOUNDING_BOX_COORD_RANGE;

	function pct(value: number): number {
		return (value / R) * 100;
	}

	let annotations = $derived(
		boxes.map((box, i) => {
			const x1 = Math.min(box.x1, box.x2);
			const y1 = Math.min(box.y1, box.y2);
			const x2 = Math.max(box.x1, box.x2);
			const y2 = Math.max(box.y1, box.y2);

			return {
				label: box.label,
				color: COLORS[i % COLORS.length],
				left: pct(x1),
				top: pct(y1),
				width: pct(x2 - x1),
				height: pct(y2 - y1)
			};
		})
	);
</script>

<figure class="bbox-figure">
	<div class="bbox-frame">
		<img src={imageSrc} {alt} class="bbox-image" />

		{#each annotations as a (a.label + a.left + a.top)}
			<div
				class="bbox-rect"
				style="left:{a.left}%; top:{a.top}%; width:{a.width}%; height:{a.height}%; border-color:{a.color};"
			>
				<span class="bbox-label" style="background-color:{a.color};">{a.label}</span>
			</div>
		{/each}
	</div>

	<figcaption class="bbox-caption">
		{annotations.length} object{annotations.length === 1 ? '' : 's'} detected
	</figcaption>
</figure>

<style>
	.bbox-figure {
		width: 100%;
		max-width: 48rem;
		margin: 1rem 0 0;
	}

	.bbox-frame {
		position: relative;
		display: inline-block;
		max-width: 100%;
		line-height: 0;
		border-radius: 0.75rem;
		overflow: hidden;
		background: hsl(var(--muted) / 0.3);
	}

	.bbox-image {
		display: block;
		max-width: 100%;
		height: auto;
	}

	.bbox-rect {
		position: absolute;
		border: 2px solid;
		border-radius: 2px;
		box-sizing: border-box;
		pointer-events: none;
		box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.35);
	}

	.bbox-label {
		position: absolute;
		bottom: 100%;
		left: -2px;
		padding: 0 4px;
		font-size: 0.625rem;
		line-height: 1.4;
		font-weight: 600;
		color: #fff;
		white-space: nowrap;
		border-radius: 2px 2px 0 0;
		text-shadow: 0 1px 1px rgba(0, 0, 0, 0.4);
		max-width: 100vw;
	}

	.bbox-caption {
		margin-top: 0.5rem;
		font-size: 0.75rem;
		color: var(--muted-foreground);
	}
</style>
