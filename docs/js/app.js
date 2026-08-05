import { initializeApp } from "https://www.gstatic.com/firebasejs/12.17.1/firebase-app.js";
import {
  getFirestore,
  collection,
  query,
  orderBy,
  limit,
  startAfter,
  getDocs,
} from "https://www.gstatic.com/firebasejs/12.17.1/firebase-firestore.js";
import { firebaseConfig } from "./firebase-config.js";

const PAGE_SIZE = 10;
const RECENT_LABEL = "최신";
const RECENT_DAY_THRESHOLD = 1;
const EXCLUDED_BLOG_NAMES = new Set(["Aws"]);
const BOOKMARKS_KEY = "tbn-bookmarks";

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const postsRef = collection(db, "posts");

const sectionsEl = document.getElementById("sections");
const loadingEl = document.getElementById("loading");
const sentinelEl = document.getElementById("scroll-sentinel");
const emptyStateEl = document.getElementById("empty-state");
const errorStateEl = document.getElementById("error-state");
const bookmarkFilterBtn = document.getElementById("bookmark-filter");

let lastDoc = null;
let hasMore = true;
let totalLoaded = 0;
let isFetching = false;
let viewMode = "all"; // "all" | "bookmarks"
let loadedPosts = []; // 이번 세션에 이미 불러온 게시글 (전체보기로 돌아올 때 재사용)

// 그룹 라벨(예: "최신", "2026. 08") -> { wrapper, list, sortValue }
const sections = new Map();

// 북마크는 Firestore 쓰기가 막혀 있어(allow write: if false) localStorage에만 저장.
let bookmarks = loadBookmarks();

function loadBookmarks() {
  try {
    const raw = localStorage.getItem(BOOKMARKS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function persistBookmarks() {
  try {
    localStorage.setItem(BOOKMARKS_KEY, JSON.stringify(bookmarks));
  } catch (error) {
    console.error("북마크를 저장하지 못했습니다.", error);
  }
}

function isBookmarked(id) {
  return bookmarks.some((b) => b.id === id);
}

function toggleBookmark(post) {
  const idx = bookmarks.findIndex((b) => b.id === post.id);
  if (idx >= 0) {
    bookmarks.splice(idx, 1);
  } else {
    bookmarks.push({
      id: post.id,
      link: post.link,
      blogName: post.blogName,
      title: post.title,
      pubDate: post.pubDate.toISOString(),
    });
  }
  persistBookmarks();
}

function getBookmarks() {
  return bookmarks
    .map((b) => ({ ...b, pubDate: new Date(b.pubDate) }))
    .sort((a, b) => b.pubDate - a.pubDate);
}

function toDate(value) {
  if (value && typeof value.toDate === "function") return value.toDate();
  if (!value) return null;
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function startOfDay(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

// MainView.groupPostsByDate와 동일한 규칙: 오늘/어제 글은 "최신"으로 묶는다.
function isRecent(pubDate) {
  const diffDays = Math.round((startOfDay(new Date()) - startOfDay(pubDate)) / 86_400_000);
  return diffDays >= 0 && diffDays <= RECENT_DAY_THRESHOLD;
}

function formatYearMonth(date) {
  const month = String(date.getMonth() + 1).padStart(2, "0");
  return `${date.getFullYear()}. ${month}`;
}

function groupKeyFor(pubDate) {
  return isRecent(pubDate) ? RECENT_LABEL : formatYearMonth(pubDate);
}

// "최신" 섹션은 항상 최상단, 나머지는 최신 월부터 내림차순.
function sortValueFor(key, pubDate) {
  return key === RECENT_LABEL ? Infinity : pubDate.getFullYear() * 12 + pubDate.getMonth();
}

function extractDomain(link) {
  try {
    return new URL(link).origin;
  } catch {
    return link;
  }
}

function faviconUrl(domain) {
  return `https://www.google.com/s2/favicons?sz=64&domain=${encodeURIComponent(domain)}`;
}

function insertSectionInOrder(section) {
  const nextSection = [...sections.values()]
    .filter((candidate) => candidate !== section)
    .find((candidate) => candidate.sortValue < section.sortValue);

  if (nextSection) {
    sectionsEl.insertBefore(section.wrapper, nextSection.wrapper);
  } else {
    sectionsEl.appendChild(section.wrapper);
  }
}

function getOrCreateSection(key, sortValue) {
  let section = sections.get(key);
  if (section) return section;

  const wrapper = document.createElement("section");
  wrapper.className = "section";

  const header = document.createElement("h2");
  header.className = "section-header";
  header.textContent = key;

  const list = document.createElement("div");
  list.className = "section-card";

  wrapper.append(header, list);

  section = { wrapper, list, sortValue };
  sections.set(key, section);
  insertSectionInOrder(section);
  return section;
}

function renderPost(post) {
  const domain = extractDomain(post.link);

  const row = document.createElement("a");
  row.className = "post-row";
  row.href = post.link;
  row.target = "_blank";
  row.rel = "noopener noreferrer";

  const title = document.createElement("div");
  title.className = "post-title";
  title.textContent = post.title;

  const favicon = document.createElement("img");
  favicon.className = "post-favicon";
  favicon.src = faviconUrl(domain);
  favicon.alt = "";
  favicon.loading = "lazy";
  // Google favicon 서비스가 도메인에 따라 간헐적으로 404를 반환하는데,
  // iOS의 CachedAsyncImage가 실패 시 플레이스홀더로 대체하는 것과 동일하게 처리.
  favicon.addEventListener("error", () => favicon.remove(), { once: true });

  const blogName = document.createElement("span");
  blogName.className = "post-blog-name";
  blogName.textContent = post.blogName;

  const meta = document.createElement("div");
  meta.className = "post-meta";
  meta.append(favicon, blogName);

  const star = document.createElement("button");
  star.type = "button";
  star.className = "post-bookmark";
  star.setAttribute("aria-label", "북마크");
  const setStarVisual = (active) => {
    star.classList.toggle("is-active", active);
    star.textContent = active ? "★" : "☆";
  };
  setStarVisual(isBookmarked(post.id));

  star.addEventListener("click", (event) => {
    // .post-row(<a>) 안에 중첩돼 있으므로 기본 링크 이동을 막아야 한다.
    event.preventDefault();
    event.stopPropagation();
    toggleBookmark(post);
    if (viewMode === "bookmarks") {
      applyBookmarksView();
    } else {
      setStarVisual(isBookmarked(post.id));
    }
  });

  row.append(title, meta, star);

  const key = groupKeyFor(post.pubDate);
  const section = getOrCreateSection(key, sortValueFor(key, post.pubDate));
  section.list.appendChild(row);
}

function setLoading(isLoading) {
  loadingEl.hidden = !isLoading;
}

async function fetchNextPage() {
  isFetching = true;
  setLoading(true);
  errorStateEl.hidden = true;

  try {
    let renderedThisRound = 0;

    // 한 페이지가 전부 제외 대상(blog_name === "Aws")이면 화면이 비어 보이지 않도록
    // 뭔가 렌더링되거나 더 가져올 페이지가 없을 때까지 이어서 가져온다.
    do {
      const constraints = [orderBy("date", "desc"), limit(PAGE_SIZE)];
      if (lastDoc) constraints.push(startAfter(lastDoc));

      const snapshot = await getDocs(query(postsRef, ...constraints));

      snapshot.forEach((doc) => {
        const data = doc.data();
        const blogName = data.blog_name;
        if (EXCLUDED_BLOG_NAMES.has(blogName)) return;

        const pubDate = toDate(data.date) ?? toDate(data.scraped_at) ?? new Date();
        const post = { id: doc.id, link: data.link, blogName, title: data.title, pubDate };
        renderPost(post);
        loadedPosts.push(post);
        renderedThisRound += 1;
        totalLoaded += 1;
      });

      lastDoc = snapshot.docs.at(-1) ?? lastDoc;
      hasMore = snapshot.size === PAGE_SIZE;
    } while (renderedThisRound === 0 && hasMore);

    emptyStateEl.hidden = totalLoaded > 0;
    if (!hasMore) scrollObserver.unobserve(sentinelEl);
  } catch (error) {
    console.error("게시글을 불러오지 못했습니다.", error);
    errorStateEl.hidden = false;
  } finally {
    isFetching = false;
    setLoading(false);
  }
}

function clearSections() {
  sections.clear();
  sectionsEl.replaceChildren();
}

function applyAllPostsView() {
  errorStateEl.hidden = true;
  emptyStateEl.textContent = "게시글이 없습니다.";
  clearSections();
  loadedPosts.forEach(renderPost);
  emptyStateEl.hidden = loadedPosts.length > 0;
}

function applyBookmarksView() {
  loadingEl.hidden = true;
  errorStateEl.hidden = true;
  emptyStateEl.textContent = "북마크된 게시글이 없습니다.";
  clearSections();
  const list = getBookmarks();
  list.forEach(renderPost);
  emptyStateEl.hidden = list.length > 0;
}

function setViewMode(mode) {
  if (mode === viewMode) return;
  viewMode = mode;
  bookmarkFilterBtn.classList.toggle("active", mode === "bookmarks");
  bookmarkFilterBtn.textContent = mode === "bookmarks" ? "★" : "☆";
  bookmarkFilterBtn.setAttribute("aria-pressed", String(mode === "bookmarks"));
  mode === "bookmarks" ? applyBookmarksView() : applyAllPostsView();
}

bookmarkFilterBtn.addEventListener("click", () => {
  setViewMode(viewMode === "all" ? "bookmarks" : "all");
});

const scrollObserver = new IntersectionObserver(
  (entries) => {
    if (viewMode !== "all") return;
    if (!entries[0].isIntersecting) return;
    if (!hasMore || isFetching) return;
    fetchNextPage();
  },
  { rootMargin: "200px" }
);
scrollObserver.observe(sentinelEl);

fetchNextPage();
