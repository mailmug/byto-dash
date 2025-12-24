export function timeAgo(date: string | Date): string {
	const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });

	const diff = (new Date(date).getTime() - Date.now()) / 1000;

	const units: [number, Intl.RelativeTimeFormatUnit][] = [
		[60, "second"],
		[60, "minute"],
		[24, "hour"],
		[7, "day"],
		[4.34524, "week"],
		[12, "month"],
		[Number.POSITIVE_INFINITY, "year"]
	];

	let duration = diff;

	for (const [amount, unit] of units) {
		if (Math.abs(duration) < amount) {
			return rtf.format(Math.round(duration), unit);
		}
		duration /= amount;
	}

	return "just now";
}
