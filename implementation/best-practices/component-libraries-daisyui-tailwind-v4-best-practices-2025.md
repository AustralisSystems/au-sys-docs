# Component Libraries (DaisyUI) & Tailwind CSS v4 Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-01-14
**DaisyUI Version**: v5+
**Tailwind CSS Version**: v4+
**Python/FastAPI Version**: Latest

This document compiles the latest best practices for building modern, beautiful web applications using component libraries (DaisyUI) and Tailwind CSS v4 based on official documentation, production code examples, and design system recommendations.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [DaisyUI Best Practices](#daisyui-best-practices)
3. [Tailwind CSS v4 Integration](#tailwind-css-v4-integration)
4. [Component Patterns](#component-patterns)
5. [Theming System](#theming-system)
6. [Design System](#design-system)
7. [Responsive Design](#responsive-design)
8. [Accessibility](#accessibility)
9. [Performance Optimization](#performance-optimization)
10. [FastAPI/Jinja2 Integration](#fastapijinja2-integration)

---

## Architecture Overview

### ✅ Modern Stack: DaisyUI + Tailwind CSS v4

```html
<!DOCTYPE html>
<html lang="en" data-theme="enterprise">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}App{% endblock %}</title>

    <!-- Tailwind CSS v4 + DaisyUI -->
    <link rel="stylesheet" href="{{ url_for('static', path='/css/app.css') }}">

    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@2.0.0"></script>

    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

**Why DaisyUI + Tailwind CSS v4?**
- ✅ **Component Library**: Pre-built, semantic components
- ✅ **Tailwind CSS v4**: Modern CSS features (@theme, @utility)
- ✅ **Theming**: Built-in theme system with 30+ themes
- ✅ **Accessibility**: WCAG-compliant components
- ✅ **Customizable**: Easy to extend and customize

---

## DaisyUI Best Practices

### ✅ Installation & Configuration

#### 1. Tailwind CSS v4 + DaisyUI Setup

```css
/* assets/styles/tailwind.css */
@import "tailwindcss";
@plugin "daisyui";
```

**Or with custom theme:**

```css
@import "tailwindcss";
@plugin "daisyui" {
  themes: enterprise --default, dark --prefersdark, light;
  logs: false;
}
```

#### 2. JavaScript Configuration (Legacy v3)

```javascript
// tailwind.config.js (for Tailwind v3)
module.exports = {
  content: [
    "./templates/**/*.html",
    "./app/**/*.py"
  ],
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        enterprise: {
          "primary": "#2563eb",
          "secondary": "#14b8a6",
          "accent": "#facc15",
          "neutral": "#1f2937",
          "base-100": "#111827",
          "info": "#0ea5e9",
          "success": "#22c55e",
          "warning": "#f97316",
          "error": "#ef4444",
        }
      },
      "light",
      "dark"
    ],
    darkTheme: "dark",
    base: true,
    styled: true,
    utils: true,
    logs: false
  }
}
```

### ✅ Component Usage

#### 1. Buttons

```html
<!-- Basic buttons -->
<button class="btn">Default</button>
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-accent">Accent</button>
<button class="btn btn-ghost">Ghost</button>
<button class="btn btn-link">Link</button>

<!-- Button sizes -->
<button class="btn btn-lg">Large</button>
<button class="btn btn-md">Medium</button>
<button class="btn btn-sm">Small</button>
<button class="btn btn-xs">Extra Small</button>

<!-- Button states -->
<button class="btn btn-primary" disabled>Disabled</button>
<button class="btn btn-primary loading">Loading</button>
<button class="btn btn-primary btn-outline">Outline</button>

<!-- Button groups -->
<div class="btn-group">
  <button class="btn btn-active">Active</button>
  <button class="btn">Button</button>
  <button class="btn">Button</button>
</div>
```

#### 2. Cards

```html
<!-- Basic card -->
<div class="card bg-base-100 shadow-xl">
  <figure>
    <img src="image.jpg" alt="Card image" />
  </figure>
  <div class="card-body">
    <h2 class="card-title">Card Title</h2>
    <p>Card description</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Action</button>
    </div>
  </div>
</div>

<!-- Card with image on side -->
<div class="card lg:card-side bg-base-100 shadow-xl">
  <figure class="lg:w-1/3">
    <img src="image.jpg" alt="Album" />
  </figure>
  <div class="card-body lg:w-2/3">
    <h2 class="card-title">Card Title</h2>
    <p>Card description</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Action</button>
    </div>
  </div>
</div>

<!-- Card with badges -->
<div class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">
      Card Title
      <div class="badge badge-secondary">NEW</div>
    </h2>
    <p>Card description</p>
  </div>
</div>
```

#### 3. Forms

```html
<!-- Form with DaisyUI -->
<form class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Form Title</h2>

    <!-- Input -->
    <label class="form-control w-full">
      <div class="label">
        <span class="label-text">Email</span>
      </div>
      <input type="email" placeholder="Enter email" class="input input-bordered w-full" />
      <div class="label">
        <span class="label-text-alt">Helper text</span>
      </div>
    </label>

    <!-- Select -->
    <label class="form-control w-full">
      <div class="label">
        <span class="label-text">Select Option</span>
      </div>
      <select class="select select-bordered w-full">
        <option disabled selected>Pick one</option>
        <option>Option 1</option>
        <option>Option 2</option>
      </select>
    </label>

    <!-- Textarea -->
    <label class="form-control">
      <div class="label">
        <span class="label-text">Message</span>
      </div>
      <textarea class="textarea textarea-bordered h-24" placeholder="Message"></textarea>
    </label>

    <!-- Checkbox -->
    <label class="label cursor-pointer">
      <span class="label-text">Remember me</span>
      <input type="checkbox" class="checkbox checkbox-primary" />
    </label>

    <!-- Radio -->
    <div class="form-control">
      <label class="label cursor-pointer">
        <span class="label-text">Option 1</span>
        <input type="radio" name="radio-option" class="radio radio-primary" checked />
      </label>
    </div>

    <!-- Toggle -->
    <label class="label cursor-pointer">
      <span class="label-text">Enable notifications</span>
      <input type="checkbox" class="toggle toggle-primary" />
    </label>

    <div class="card-actions justify-end">
      <button type="submit" class="btn btn-primary">Submit</button>
    </div>
  </div>
</form>
```

#### 4. Modals

```html
<!-- Modal trigger -->
<button class="btn" onclick="my_modal.showModal()">Open Modal</button>

<!-- Modal -->
<dialog id="my_modal" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Modal Title</h3>
    <p class="py-4">Modal content goes here</p>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn">Close</button>
        <button class="btn btn-primary">Save</button>
      </form>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>

<!-- With Alpine.js -->
<div x-data="{ open: false }">
  <button @click="open = true" class="btn">Open Modal</button>

  <dialog x-show="open"
          @click.outside="open = false"
          class="modal">
    <div class="modal-box">
      <h3 class="font-bold text-lg">Modal Title</h3>
      <p class="py-4">Modal content</p>
      <div class="modal-action">
        <button @click="open = false" class="btn">Close</button>
      </div>
    </div>
  </dialog>
</div>
```

#### 5. Navigation

```html
<!-- Navbar -->
<div class="navbar bg-base-100 shadow-lg">
  <div class="flex-1">
    <a class="btn btn-ghost text-xl">Logo</a>
  </div>
  <div class="flex-none">
    <ul class="menu menu-horizontal px-1">
      <li><a>Link 1</a></li>
      <li><a>Link 2</a></li>
      <li>
        <details>
          <summary>Parent</summary>
          <ul class="p-2 bg-base-100">
            <li><a>Submenu 1</a></li>
            <li><a>Submenu 2</a></li>
          </ul>
        </details>
      </li>
    </ul>
  </div>
</div>

<!-- Breadcrumbs -->
<div class="breadcrumbs">
  <ul>
    <li><a>Home</a></li>
    <li><a>Documents</a></li>
    <li>Add Document</li>
  </ul>
</div>

<!-- Tabs -->
<div role="tablist" class="tabs tabs-bordered">
  <input type="radio" name="my_tabs_1" role="tab" class="tab" aria-label="Tab 1" checked />
  <div role="tabpanel" class="tab-content p-4">Tab content 1</div>

  <input type="radio" name="my_tabs_1" role="tab" class="tab" aria-label="Tab 2" />
  <div role="tabpanel" class="tab-content p-4">Tab content 2</div>
</div>
```

#### 6. Tables

```html
<!-- Table -->
<div class="overflow-x-auto">
  <table class="table">
    <thead>
      <tr>
        <th></th>
        <th>Name</th>
        <th>Email</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th>1</th>
        <td>John Doe</td>
        <td>john@example.com</td>
        <td>
          <button class="btn btn-sm btn-primary">Edit</button>
          <button class="btn btn-sm btn-error">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Table with zebra stripes -->
<table class="table table-zebra">
  <!-- ... -->
</table>

<!-- Table with hover -->
<table class="table table-hover">
  <!-- ... -->
</table>
```

#### 7. Alerts & Notifications

```html
<!-- Alert -->
<div role="alert" class="alert alert-info">
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
  </svg>
  <span>Info alert</span>
</div>

<!-- Alert types -->
<div class="alert alert-success">Success</div>
<div class="alert alert-warning">Warning</div>
<div class="alert alert-error">Error</div>

<!-- Toast (with Alpine.js) -->
<div x-data="{ show: false }"
     x-show="show"
     x-transition
     class="toast toast-top toast-end">
  <div class="alert alert-success">
    <span>Message sent!</span>
  </div>
</div>
```

#### 8. Badges & Indicators

```html
<!-- Badges -->
<div class="badge">Badge</div>
<div class="badge badge-primary">Primary</div>
<div class="badge badge-secondary">Secondary</div>
<div class="badge badge-accent">Accent</div>
<div class="badge badge-ghost">Ghost</div>

<!-- Badge sizes -->
<div class="badge badge-lg">Large</div>
<div class="badge badge-md">Medium</div>
<div class="badge badge-sm">Small</div>
<div class="badge badge-xs">Extra Small</div>

<!-- Badge with number -->
<div class="badge badge-primary badge-lg">99+</div>

<!-- Indicator -->
<div class="indicator">
  <span class="indicator-item badge badge-secondary">new</span>
  <div class="grid w-32 h-32 bg-base-300 place-items-center">content</div>
</div>
```

---

## Tailwind CSS v4 Integration

### ✅ Best Practices

#### 1. @theme Directive

```css
@import "tailwindcss";
@plugin "daisyui";

@theme {
  /* Custom fonts */
  --font-family-display: "Satoshi", "sans-serif";
  --font-family-body: "Inter", "sans-serif";

  /* Custom breakpoints */
  --breakpoint-3xl: 1920px;

  /* Custom colors (OKLCH format) */
  --color-brand-primary: oklch(55% 0.3 240);
  --color-brand-secondary: oklch(70% 0.25 200);

  /* Custom spacing */
  --spacing-xs: 0.25rem;
  --spacing-xl: 1.5rem;
}
```

#### 2. @utility Directive

```css
/* Custom component utilities */
@utility btn-custom {
  @apply btn btn-primary;
  background: linear-gradient(45deg, var(--color-primary), var(--color-secondary));
  border: none;
}

@utility card-premium {
  @apply card bg-base-100 shadow-xl;
  background: linear-gradient(to bottom right, var(--color-primary), var(--color-accent));
  color: white;
}
```

#### 3. Combining DaisyUI with Tailwind Utilities

```html
<!-- DaisyUI components + Tailwind utilities -->
<div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow">
  <div class="card-body p-6 lg:p-8">
    <h2 class="card-title text-2xl lg:text-3xl">Title</h2>
    <p class="text-base-content/70">Description</p>
    <div class="card-actions justify-end mt-4">
      <button class="btn btn-primary btn-sm lg:btn-md">Action</button>
    </div>
  </div>
</div>
```

---

## Component Patterns

### ✅ Best Practices

#### 1. Component Composition

```html
<!-- Reusable card component pattern -->
<div class="card bg-base-100 shadow-xl hover:shadow-2xl transition-all">
  <div class="card-body">
    <div class="flex items-center justify-between mb-4">
      <h2 class="card-title text-xl">Title</h2>
      <div class="badge badge-primary">New</div>
    </div>
    <p class="text-base-content/70 mb-4">Description</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary btn-sm">Action</button>
    </div>
  </div>
</div>
```

#### 2. Stat Cards

```html
<!-- Stat card pattern -->
<div class="stat bg-base-100 shadow-lg rounded-lg p-6">
  <div class="stat-figure text-primary">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-8 h-8 stroke-current">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
    </svg>
  </div>
  <div class="stat-title">Total Users</div>
  <div class="stat-value text-primary">31K</div>
  <div class="stat-desc">21% more than last month</div>
</div>
```

#### 3. Form Patterns

```html
<!-- Form with validation -->
<form class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Form Title</h2>

    <!-- Input with label and error -->
    <label class="form-control w-full">
      <div class="label">
        <span class="label-text">Email</span>
        <span class="label-text-alt text-error">Required</span>
      </div>
      <input type="email"
             placeholder="email@example.com"
             class="input input-bordered w-full input-error" />
      <div class="label">
        <span class="label-text-alt text-error">Invalid email format</span>
      </div>
    </label>

    <!-- Input with icon -->
    <label class="form-control w-full">
      <div class="label">
        <span class="label-text">Search</span>
      </div>
      <div class="relative">
        <input type="text"
               placeholder="Search..."
               class="input input-bordered w-full pl-10" />
        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-base-content/50"
             fill="none"
             stroke="currentColor"
             viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
      </div>
    </label>
  </div>
</form>
```

#### 4. Loading States

```html
<!-- Loading button -->
<button class="btn btn-primary loading">Loading</button>

<!-- Loading spinner -->
<div class="flex justify-center items-center h-64">
  <span class="loading loading-spinner loading-lg"></span>
</div>

<!-- Skeleton loading -->
<div class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <div class="skeleton h-4 w-3/4 mb-4"></div>
    <div class="skeleton h-4 w-full mb-2"></div>
    <div class="skeleton h-4 w-5/6"></div>
  </div>
</div>
```

---

## Theming System

### ✅ Best Practices

#### 1. Theme Configuration

```css
/* Custom theme with Tailwind CSS v4 */
@import "tailwindcss";
@plugin "daisyui";
@plugin "daisyui/theme" {
  name: "enterprise";
  default: true;
  prefersdark: false;
  color-scheme: light;

  --color-base-100: oklch(98% 0.02 240);
  --color-base-200: oklch(95% 0.03 240);
  --color-base-300: oklch(92% 0.04 240);
  --color-base-content: oklch(20% 0.05 240);

  --color-primary: oklch(55% 0.3 240);
  --color-primary-content: oklch(98% 0.01 240);

  --color-secondary: oklch(70% 0.25 200);
  --color-secondary-content: oklch(98% 0.01 200);

  --color-accent: oklch(65% 0.25 160);
  --color-accent-content: oklch(98% 0.01 160);

  --color-neutral: oklch(50% 0.05 240);
  --color-neutral-content: oklch(98% 0.01 240);

  --color-info: oklch(70% 0.2 220);
  --color-info-content: oklch(98% 0.01 220);

  --color-success: oklch(65% 0.25 140);
  --color-success-content: oklch(98% 0.01 140);

  --color-warning: oklch(80% 0.25 80);
  --color-warning-content: oklch(20% 0.05 80);

  --color-error: oklch(65% 0.3 30);
  --color-error-content: oklch(98% 0.01 30);

  --radius-selector: 0.5rem;
  --radius-field: 0.25rem;
  --radius-box: 0.5rem;

  --size-selector: 0.25rem;
  --size-field: 0.25rem;

  --border: 1px;
  --depth: 1;
  --noise: 0;
}
```

#### 2. Theme Switching

```html
<!-- Theme selector -->
<select class="select select-bordered" data-choose-theme>
  <option value="light">Light</option>
  <option value="dark">Dark</option>
  <option value="enterprise">Enterprise</option>
  <option value="cupcake">Cupcake</option>
</select>

<!-- With Alpine.js -->
<div x-data="{ theme: 'light' }">
  <select x-model="theme"
          @change="$dispatch('theme-change', theme)"
          class="select select-bordered">
    <option value="light">Light</option>
    <option value="dark">Dark</option>
    <option value="enterprise">Enterprise</option>
  </select>
</div>

<script>
document.addEventListener('theme-change', (e) => {
  document.documentElement.setAttribute('data-theme', e.detail);
  localStorage.setItem('theme', e.detail);
});

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
</script>
```

#### 3. Using Theme Variables

```css
/* Access DaisyUI theme variables */
.custom-element {
  background-color: var(--color-primary);
  color: var(--color-primary-content);
  border-radius: var(--radius-box);
}

.custom-card {
  background: var(--color-base-100);
  color: var(--color-base-content);
  border: var(--border) solid var(--color-base-200);
}

.success-message {
  background-color: var(--color-success);
  color: var(--color-success-content);
}
```

---

## Design System

### ✅ Best Practices

#### 1. Color System

```html
<!-- Semantic colors -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-accent">Accent</button>
<button class="btn btn-neutral">Neutral</button>

<!-- State colors -->
<div class="alert alert-info">Info</div>
<div class="alert alert-success">Success</div>
<div class="alert alert-warning">Warning</div>
<div class="alert alert-error">Error</div>

<!-- Base colors -->
<div class="bg-base-100">Base 100</div>
<div class="bg-base-200">Base 200</div>
<div class="bg-base-300">Base 300</div>
<div class="text-base-content">Base Content</div>
```

#### 2. Typography

```html
<!-- Headings -->
<h1 class="text-4xl font-bold">Heading 1</h1>
<h2 class="text-3xl font-semibold">Heading 2</h2>
<h3 class="text-2xl font-medium">Heading 3</h3>

<!-- Body text -->
<p class="text-base">Body text</p>
<p class="text-sm text-base-content/70">Small text</p>
<p class="text-xs text-base-content/50">Extra small text</p>

<!-- With DaisyUI card title -->
<h2 class="card-title">Card Title</h2>
```

#### 3. Spacing System

```html
<!-- Consistent spacing -->
<div class="card-body p-6">
  <div class="space-y-4">
    <div>Item 1</div>
    <div>Item 2</div>
  </div>
</div>

<!-- Responsive spacing -->
<div class="p-4 md:p-6 lg:p-8">
  Content
</div>
```

---

## Responsive Design

### ✅ Best Practices

#### 1. Responsive Components

```html
<!-- Responsive card -->
<div class="card lg:card-side bg-base-100 shadow-xl">
  <figure class="w-full lg:w-1/3">
    <img src="image.jpg" alt="Album" />
  </figure>
  <div class="card-body w-full lg:w-2/3">
    <h2 class="card-title">Card Title</h2>
    <p>Card description</p>
  </div>
</div>

<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="card bg-base-100">Card 1</div>
  <div class="card bg-base-100">Card 2</div>
  <div class="card bg-base-100">Card 3</div>
</div>

<!-- Responsive navbar -->
<div class="navbar bg-base-100">
  <div class="navbar-start">
    <div class="dropdown">
      <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
        </svg>
      </div>
      <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
        <li><a>Home</a></li>
        <li><a>About</a></li>
      </ul>
    </div>
    <a class="btn btn-ghost text-xl">Logo</a>
  </div>
  <div class="navbar-center hidden lg:flex">
    <ul class="menu menu-horizontal px-1">
      <li><a>Home</a></li>
      <li><a>About</a></li>
    </ul>
  </div>
</div>
```

#### 2. Container Queries (Tailwind v4)

```html
<!-- Container queries -->
<div class="@container">
  <div class="grid grid-cols-3 @max-md:grid-cols-1">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
  </div>
</div>
```

---

## Accessibility

### ✅ Best Practices

#### 1. Semantic HTML

```html
<!-- Use semantic elements -->
<nav class="navbar" role="navigation" aria-label="Main navigation">
  <ul class="menu menu-horizontal">
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- Form labels -->
<label class="form-control">
  <div class="label">
    <span class="label-text">Email</span>
  </div>
  <input type="email"
         aria-label="Email address"
         aria-required="true"
         class="input input-bordered" />
</label>

<!-- Button with aria -->
<button class="btn btn-primary"
        aria-label="Submit form"
        aria-busy="false">
  Submit
</button>
```

#### 2. ARIA Attributes

```html
<!-- Alert with role -->
<div role="alert" class="alert alert-error">
  <span>Error message</span>
</div>

<!-- Modal with aria -->
<dialog id="modal"
        class="modal"
        aria-labelledby="modal-title"
        aria-describedby="modal-description">
  <div class="modal-box">
    <h3 id="modal-title" class="font-bold text-lg">Modal Title</h3>
    <p id="modal-description">Modal description</p>
  </div>
</dialog>

<!-- Loading state -->
<button class="btn btn-primary loading"
        aria-busy="true"
        aria-label="Loading">
  Loading
</button>
```

#### 3. Keyboard Navigation

```html
<!-- Focusable elements -->
<button class="btn btn-primary focus:ring-2 focus:ring-primary focus:ring-offset-2">
  Focusable Button
</button>

<!-- Skip link -->
<a href="#main-content" class="btn btn-ghost sr-only focus:not-sr-only">
  Skip to main content
</a>
```

---

## Performance Optimization

### ✅ Best Practices

#### 1. Component Tree Shaking

```css
/* Include only needed components */
@plugin "daisyui" {
  include: button, card, modal, navbar, dropdown, form-control, table, alert;
  exclude: carousel, artboard;
}
```

#### 2. CSS Optimization

```bash
# Build command with minification
npx tailwindcss -i assets/styles/tailwind.css -o app/static/css/app.css --minify
```

#### 3. Lazy Loading Components

```html
<!-- Load components on demand -->
<div hx-get="/components/modal"
     hx-trigger="click"
     hx-target="#modal-container">
  Open Modal
</div>
```

---

## FastAPI/Jinja2 Integration

### ✅ Best Practices

#### 1. Component Macros

```jinja
<!-- components/button.html -->
{% macro button(text, variant="primary", size="md", **kwargs) %}
<button class="btn btn-{{ variant }} btn-{{ size }} {{ kwargs.get('class', '') }}"
        {% for key, value in kwargs.items() %}
            {% if key != 'class' %}
                {{ key }}="{{ value }}"
            {% endif %}
        {% endfor %}>
    {{ text }}
</button>
{% endmacro %}

<!-- Usage -->
{% import "components/button.html" as btn %}
{{ btn.button("Submit", variant="primary", hx_post="/api/submit") }}
```

#### 2. Card Component

```jinja
<!-- components/card.html -->
{% macro card(title, content, footer=None, image=None) %}
<div class="card bg-base-100 shadow-xl">
    {% if image %}
    <figure>
        <img src="{{ image }}" alt="{{ title }}" />
    </figure>
    {% endif %}
    <div class="card-body">
        <h2 class="card-title">{{ title }}</h2>
        <p>{{ content }}</p>
        {% if footer %}
        <div class="card-actions justify-end">
            {{ footer }}
        </div>
        {% endif %}
    </div>
</div>
{% endmacro %}
```

#### 3. Form Components

```jinja
<!-- components/form_field.html -->
{% macro form_field(name, label, type="text", placeholder="", required=false, error=None) %}
<label class="form-control w-full">
    <div class="label">
        <span class="label-text">{{ label }}</span>
        {% if required %}
        <span class="label-text-alt text-error">Required</span>
        {% endif %}
    </div>
    <input type="{{ type }}"
           name="{{ name }}"
           placeholder="{{ placeholder }}"
           class="input input-bordered w-full {% if error %}input-error{% endif %}"
           {% if required %}required{% endif %} />
    {% if error %}
    <div class="label">
        <span class="label-text-alt text-error">{{ error }}</span>
    </div>
    {% endif %}
</label>
{% endmacro %}
```

---

## Summary Checklist

### DaisyUI
- [ ] DaisyUI installed and configured
- [ ] Theme system configured
- [ ] Components used semantically
- [ ] Custom theme created (if needed)
- [ ] Component tree shaking configured

### Tailwind CSS v4
- [ ] @theme directive used for configuration
- [ ] @utility directive for custom components
- [ ] Modern CSS features utilized
- [ ] Container queries used where appropriate
- [ ] Variant composition used

### Components
- [ ] Buttons with proper variants
- [ ] Cards with consistent structure
- [ ] Forms with validation styling
- [ ] Modals with proper accessibility
- [ ] Navigation with responsive design
- [ ] Tables with proper styling
- [ ] Alerts and notifications

### Theming
- [ ] Custom theme defined
- [ ] Theme switching implemented
- [ ] Theme variables used in custom CSS
- [ ] Dark mode support

### Accessibility
- [ ] Semantic HTML used
- [ ] ARIA attributes added
- [ ] Keyboard navigation supported
- [ ] Focus states styled

### Performance
- [ ] Component tree shaking
- [ ] CSS minification
- [ ] Lazy loading implemented
- [ ] Optimized bundle size

---

## References

- [DaisyUI Documentation](https://daisyui.com/)
- [Tailwind CSS v4 Documentation](https://tailwindcss.com/docs)
- [DaisyUI Components](https://daisyui.com/components/)

---

**Note:** This document is based on DaisyUI v5+, Tailwind CSS v4+, and latest best practices. Always refer to official documentation for the most up-to-date information.
