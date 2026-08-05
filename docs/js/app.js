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

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const postsRef = collection(db, "posts");

const sectionsEl = document.getElementById("sections");
const loadingEl = document.getElementById("loading");
const loadMoreBtn = document.getElementById("load-more");
const emptyStateEl = document.getElementById("empty-state");
const errorStateEl = document.getElementById("error-state");

let lastDoc = null;
let hasMore = true;
let totalLoaded = 0;

// 그룹 라벨(예: "최신", "2026. 08") -> { wrapper, list, sortValue }
const sections = new Map();

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

  row.append(title, meta);

  const key = groupKeyFor(post.pubDate);
  const section = getOrCreateSection(key, sortValueFor(key, post.pubDate));
  section.list.appendChild(row);
}

function setLoading(isLoading) {
  loadingEl.hidden = !isLoading;
  if (isLoading) loadMoreBtn.hidden = true;
}

async function fetchNextPage() {
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
        renderPost({ link: data.link, blogName, title: data.title, pubDate });
        renderedThisRound += 1;
        totalLoaded += 1;
      });

      lastDoc = snapshot.docs.at(-1) ?? lastDoc;
      hasMore = snapshot.size === PAGE_SIZE;
    } while (renderedThisRound === 0 && hasMore);

    emptyStateEl.hidden = totalLoaded > 0;
    loadMoreBtn.hidden = !hasMore;
  } catch (error) {
    console.error("게시글을 불러오지 못했습니다.", error);
    errorStateEl.hidden = false;
    loadMoreBtn.hidden = true;
  } finally {
    setLoading(false);
  }
}

loadMoreBtn.addEventListener("click", fetchNextPage);

fetchNextPage();
