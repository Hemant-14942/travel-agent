const ACCESS_KEY = process.env.NEXT_PUBLIC_UNSPLASH_ACCESS_KEY ?? "";

export interface UnsplashPhoto {
  url: string;          // full-size
  thumb: string;        // 400px
  regular: string;      // 1080px wide — best for hero
  credit: string;       // photographer name
  creditLink: string;   // photographer profile
  altDescription: string;
}

const _cache = new Map<string, UnsplashPhoto | null>();

async function _searchOne(query: string): Promise<UnsplashPhoto | null> {
  const encoded = encodeURIComponent(query);
  const res = await fetch(
    `https://api.unsplash.com/search/photos?query=${encoded}&per_page=3&orientation=landscape`,
    { headers: { Authorization: `Client-ID ${ACCESS_KEY}` } },
  );
  if (!res.ok) return null;
  const json = await res.json();
  const photo = json.results?.[0];
  if (!photo) return null;
  return {
    url: photo.urls.full,
    thumb: photo.urls.thumb,
    regular: photo.urls.regular,
    credit: photo.user?.name ?? "Unknown",
    creditLink: photo.user?.links?.html ?? "#",
    altDescription: photo.alt_description ?? query,
  };
}

/**
 * Fetch a hero photo for a destination.
 * Tries multiple progressively broader queries so small cities
 * (e.g. "Panaji") fall back to the wider region (e.g. "Goa").
 */
export async function fetchDestinationPhoto(
  /** Primary search term — typically the resolved city name */
  primary: string,
  /** Fallback term — typically the user-entered destination */
  fallback?: string,
): Promise<UnsplashPhoto | null> {
  if (!ACCESS_KEY) return null;

  const cacheKey = `${primary}::${fallback ?? ""}`;
  if (_cache.has(cacheKey)) return _cache.get(cacheKey) ?? null;

  // Build a priority list of queries, deduped.
  const queries: string[] = [];
  if (primary)   queries.push(`${primary} travel`);
  if (fallback && fallback.toLowerCase() !== primary.toLowerCase())
    queries.push(`${fallback} travel`);
  if (primary)   queries.push(primary);        // bare name — wider results
  if (fallback)  queries.push(fallback);
  queries.push("travel destination nature");   // last resort — always has results

  try {
    for (const q of queries) {
      const photo = await _searchOne(q);
      if (photo) {
        _cache.set(cacheKey, photo);
        return photo;
      }
    }
    _cache.set(cacheKey, null);
    return null;
  } catch {
    _cache.set(cacheKey, null);
    return null;
  }
}
