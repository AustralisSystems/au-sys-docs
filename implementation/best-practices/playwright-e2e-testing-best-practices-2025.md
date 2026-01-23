# Playwright E2E Testing Best Practices 2025
**Version**: v1.0.0
**Last Updated**: 2025-11-18
**Playwright Version**: ^1.40.0+
**TypeScript/JavaScript**: Latest

This document compiles best practices for comprehensive end-to-end (E2E) testing with Playwright, focusing on UX/UI functionality, user interactions, component behavior, and enterprise-grade test coverage for HTMX-based web applications.

---

## Table of Contents

1. [Test Architecture & Organization](#test-architecture--organization)
2. [Page Object Model (POM)](#page-object-model-pom)
3. [Component Testing Patterns](#component-testing-patterns)
4. [User Interaction Testing](#user-interaction-testing)
5. [HTMX Functionality Testing](#htmx-functionality-testing)
6. [Form Testing](#form-testing)
7. [Data Operations Testing](#data-operations-testing)
8. [UI State & Feedback Testing](#ui-state--feedback-testing)
9. [Visual Regression Testing](#visual-regression-testing)
10. [Accessibility Testing](#accessibility-testing)
11. [Performance Testing](#performance-testing)
12. [Test Data Management](#test-data-management)
13. [Error Handling & Edge Cases](#error-handling--edge-cases)
14. [CI/CD Integration](#cicd-integration)

---

## Test Architecture & Organization

### ✅ Best Practices

#### 1. Directory Structure

Organize tests following a clear, maintainable structure:

```
tests/
├── e2e/
│   ├── fixtures/
│   │   ├── auth.fixture.ts          # Authentication helpers
│   │   ├── data.fixture.ts           # Test data generators
│   │   └── server.fixture.ts        # Test server setup
│   ├── page-objects/
│   │   ├── base.page.ts             # Base page object
│   │   ├── dashboard.page.ts        # Page-specific objects
│   │   ├── workflows.page.ts
│   │   └── components/
│   │       ├── interactive-card.page.ts
│   │       └── interactive-button.page.ts
│   ├── specs/
│   │   ├── navigation.spec.ts       # Navigation tests
│   │   ├── pages/                   # Page-specific tests
│   │   ├── components/              # Component tests
│   │   ├── htmx/                    # HTMX functionality tests
│   │   ├── accessibility/           # Accessibility tests
│   │   └── visual/                  # Visual regression tests
│   ├── utils/
│   │   ├── helpers.ts               # Test utilities
│   │   ├── assertions.ts           # Custom assertions
│   │   └── constants.ts             # Test constants
│   └── playwright.config.ts         # Playwright configuration
```

#### 2. Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e/specs',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'test-results/html-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:8080',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  webServer: {
    command: 'uvicorn app:app --reload --host 0.0.0.0 --port 8080',
    url: 'http://localhost:8080',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

#### 3. Test Fixtures

```typescript
// fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page, baseURL }, use) => {
    // Login flow
    await page.goto(`${baseURL}/login`);
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass');
    await page.click('button[type="submit"]');
    await page.waitForURL(`${baseURL}/dashboard`);

    await use(page);

    // Cleanup
    await page.context().clearCookies();
  },
});

// Usage in tests
test('dashboard shows user data', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/dashboard');
  // Test authenticated functionality
});
```

---

## Page Object Model (POM)

### ✅ Best Practices

#### 1. Base Page Object

Create a base page object with common functionality:

```typescript
// page-objects/base.page.ts
import { Page, Locator, expect } from '@playwright/test';

export class BasePage {
  constructor(protected page: Page) {}

  async goto(path: string = ''): Promise<void> {
    await this.page.goto(path);
    await this.waitForLoad();
  }

  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
    await this.waitForHTMXComplete();
  }

  async waitForHTMXComplete(): Promise<void> {
    // Wait for HTMX requests to complete
    await this.page.waitForFunction(() => {
      return !document.querySelector('.htmx-request');
    }, { timeout: 10000 });
  }

  async getTitle(): Promise<string> {
    return await this.page.title();
  }

  getUrl(): string {
    return this.page.url();
  }

  async takeScreenshot(name: string): Promise<Buffer> {
    return await this.page.screenshot({ fullPage: true });
  }

  async isVisible(selector: string): Promise<boolean> {
    return await this.page.locator(selector).isVisible();
  }

  async waitForElement(selector: string, timeout = 5000): Promise<Locator> {
    const element = this.page.locator(selector);
    await element.waitFor({ state: 'visible', timeout });
    return element;
  }
}
```

#### 2. Page-Specific Objects

Extend base page for page-specific functionality:

```typescript
// page-objects/dashboard.page.ts
import { BasePage } from './base.page';
import { Page, Locator } from '@playwright/test';

export class DashboardPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  // Selectors
  private get statsCards(): Locator {
    return this.page.locator('[data-testid="stats-card"]');
  }

  private get dataTable(): Locator {
    return this.page.locator('[data-testid="data-table"]');
  }

  private get refreshButton(): Locator {
    return this.page.locator('button[data-testid="refresh-data"]');
  }

  // Methods
  async getStatsCardCount(): Promise<number> {
    return await this.statsCards.count();
  }

  async clickStatsCard(index: number): Promise<void> {
    await this.statsCards.nth(index).click();
    await this.waitForHTMXComplete();
  }

  async hoverStatsCard(index: number): Promise<void> {
    await this.statsCards.nth(index).hover();
  }

  async sortTableByColumn(columnName: string): Promise<void> {
    const columnHeader = this.page.locator(
      `[data-testid="table-header-${columnName}"]`
    );
    await columnHeader.click();
    await this.waitForHTMXComplete();
  }

  async filterTable(filterText: string): Promise<void> {
    const filterInput = this.page.locator('[data-testid="table-filter"]');
    await filterInput.fill(filterText);
    await this.waitForHTMXComplete();
  }

  async clickPaginationNext(): Promise<void> {
    await this.page.locator('[data-testid="pagination-next"]').click();
    await this.waitForHTMXComplete();
  }

  async refreshData(): Promise<void> {
    await this.refreshButton.click();
    // Wait for loading state
    await this.page.waitForSelector('[data-testid="loading-indicator"]', {
      state: 'visible',
    });
    // Wait for loading to complete
    await this.page.waitForSelector('[data-testid="loading-indicator"]', {
      state: 'hidden',
    });
    await this.waitForHTMXComplete();
  }

  async verifyDataReadable(): Promise<boolean> {
    const tableRows = this.page.locator('[data-testid="table-row"]');
    const count = await tableRows.count();

    for (let i = 0; i < count; i++) {
      const row = tableRows.nth(i);
      const text = await row.textContent();
      if (!text || text.trim().length === 0) {
        return false;
      }
    }
    return true;
  }
}
```

---

## Component Testing Patterns

### ✅ Best Practices

#### 1. Component Object Model

Create reusable component objects:

```typescript
// page-objects/components/interactive-card.page.ts
import { Page, Locator, expect } from '@playwright/test';

export class InteractiveCard {
  constructor(
    private page: Page,
    private selector: string
  ) {}

  private get card(): Locator {
    return this.page.locator(this.selector);
  }

  async click(): Promise<void> {
    await this.card.click();
    await this.waitForHTMXComplete();
  }

  async hover(): Promise<void> {
    await this.card.hover();
    // Wait for tooltip or additional info to appear
    await this.page.waitForTimeout(300);
  }

  async isExpanded(): Promise<boolean> {
    return await this.card.getAttribute('aria-expanded') === 'true';
  }

  async expand(): Promise<void> {
    if (!(await this.isExpanded())) {
      await this.card.click();
      await this.page.waitForSelector(
        `${this.selector}[aria-expanded="true"]`,
        { timeout: 5000 }
      );
    }
  }

  async collapse(): Promise<void> {
    if (await this.isExpanded()) {
      await this.card.click();
      await this.page.waitForSelector(
        `${this.selector}[aria-expanded="false"]`,
        { timeout: 5000 }
      );
    }
  }

  async isSelected(): Promise<boolean> {
    return await this.card.getAttribute('aria-selected') === 'true';
  }

  async getData(): Promise<string> {
    return await this.card.textContent() || '';
  }

  async verifyVisualFeedback(): Promise<void> {
    // Test hover state
    await this.hover();
    const hoverClass = await this.card.getAttribute('class');
    expect(hoverClass).toContain('hover:');

    // Test active state
    await this.click();
    const activeClass = await this.card.getAttribute('class');
    expect(activeClass).toContain('active');
  }

  private async waitForHTMXComplete(): Promise<void> {
    await this.page.waitForFunction(() => {
      return !document.querySelector('.htmx-request');
    }, { timeout: 10000 });
  }
}
```

#### 2. Interactive Button Component

```typescript
// page-objects/components/interactive-button.page.ts
export class InteractiveButton {
  constructor(
    private page: Page,
    private selector: string
  ) {}

  private get button(): Locator {
    return this.page.locator(this.selector);
  }

  async click(): Promise<void> {
    await this.button.click();
    await this.waitForHTMXComplete();
  }

  async isDisabled(): Promise<boolean> {
    return await this.button.isDisabled();
  }

  async isLoading(): Promise<boolean> {
    const loadingIndicator = this.button.locator('[data-testid="loading"]');
    return await loadingIndicator.isVisible();
  }

  async waitForLoadingComplete(): Promise<void> {
    await this.page.waitForSelector(
      `${this.selector} [data-testid="loading"]`,
      { state: 'hidden', timeout: 10000 }
    );
  }

  async verifyActionTriggered(expectedUrl?: string): Promise<void> {
    if (expectedUrl) {
      await this.page.waitForURL(expectedUrl, { timeout: 5000 });
    }
    // Verify any expected side effects
  }

  async verifyVisualFeedback(): Promise<void> {
    // Test hover
    await this.button.hover();
    const hoverStyles = await this.button.evaluate((el) => {
      return window.getComputedStyle(el).cursor;
    });
    expect(hoverStyles).toBe('pointer');

    // Test active state
    await this.button.click({ delay: 100 });
    const activeStyles = await this.button.evaluate((el) => {
      return window.getComputedStyle(el).transform;
    });
    // Verify button provides visual feedback
  }
}
```

#### 3. Interactive Data Table Component

```typescript
// page-objects/components/interactive-data-table.page.ts
export class InteractiveDataTable {
  constructor(
    private page: Page,
    private selector: string
  ) {}

  async sortByColumn(columnName: string, direction: 'asc' | 'desc' = 'asc'): Promise<void> {
    const header = this.page.locator(
      `${this.selector} [data-testid="column-${columnName}"]`
    );

    // Click to toggle sort
    await header.click();
    await this.waitForHTMXComplete();

    // If direction is desc, click again
    if (direction === 'desc') {
      await header.click();
      await this.waitForHTMXComplete();
    }

    // Verify sort indicator
    const sortIndicator = header.locator('[data-testid="sort-indicator"]');
    await expect(sortIndicator).toBeVisible();
  }

  async filter(filterText: string): Promise<void> {
    const filterInput = this.page.locator(
      `${this.selector} [data-testid="table-filter"]`
    );
    await filterInput.fill(filterText);
    await this.waitForHTMXComplete();

    // Verify filtered results
    const rows = this.page.locator(`${this.selector} [data-testid="table-row"]`);
    const count = await rows.count();
    expect(count).toBeGreaterThan(0);
  }

  async selectRow(index: number): Promise<void> {
    const row = this.page.locator(
      `${this.selector} [data-testid="table-row"]`
    ).nth(index);
    await row.click();

    // Verify selection state
    await expect(row).toHaveAttribute('aria-selected', 'true');
  }

  async paginateToPage(pageNumber: number): Promise<void> {
    const pageButton = this.page.locator(
      `${this.selector} [data-testid="pagination-page-${pageNumber}"]`
    );
    await pageButton.click();
    await this.waitForHTMXComplete();

    // Verify current page
    await expect(pageButton).toHaveAttribute('aria-current', 'page');
  }

  async verifyDataReadable(): Promise<boolean> {
    const rows = this.page.locator(`${this.selector} [data-testid="table-row"]`);
    const count = await rows.count();

    for (let i = 0; i < count; i++) {
      const row = rows.nth(i);
      const text = await row.textContent();
      if (!text || text.trim().length === 0) {
        return false;
      }

      // Verify data is formatted correctly
      const cells = row.locator('td');
      const cellCount = await cells.count();
      if (cellCount === 0) {
        return false;
      }
    }
    return true;
  }
}
```

---

## User Interaction Testing

### ✅ Best Practices

#### 1. Testing User Workflows

Test complete user journeys, not just individual actions:

```typescript
// specs/pages/workflows.spec.ts
import { test, expect } from '@playwright/test';
import { WorkflowsPage } from '../../page-objects/workflows.page';

test.describe('Workflows User Journey', () => {
  test('complete workflow creation and execution flow', async ({ page }) => {
    const workflowsPage = new WorkflowsPage(page);

    // Navigate to workflows page
    await workflowsPage.goto('/workflows');

    // Click create workflow button
    await workflowsPage.clickCreateWorkflow();

    // Fill workflow form
    await workflowsPage.fillWorkflowForm({
      name: 'Test Workflow',
      description: 'Test workflow description',
      steps: ['step1', 'step2'],
    });

    // Submit form
    await workflowsPage.submitWorkflowForm();

    // Verify success message
    await expect(workflowsPage.successMessage).toBeVisible();

    // Verify workflow appears in list
    await expect(workflowsPage.getWorkflowByName('Test Workflow')).toBeVisible();

    // Execute workflow
    await workflowsPage.executeWorkflow('Test Workflow');

    // Verify execution started
    await expect(workflowsPage.getWorkflowStatus('Test Workflow')).toContainText('Running');

    // Wait for completion
    await workflowsPage.waitForWorkflowCompletion('Test Workflow');

    // Verify final status
    await expect(workflowsPage.getWorkflowStatus('Test Workflow')).toContainText('Completed');
  });
});
```

#### 2. Testing Component Interactions

```typescript
// specs/components/interactive-card.spec.ts
import { test, expect } from '@playwright/test';
import { InteractiveCard } from '../../page-objects/components/interactive-card.page';

test.describe('Interactive Card Functionality', () => {
  test('card click triggers correct action', async ({ page }) => {
    await page.goto('/dashboard');

    const card = new InteractiveCard(page, '[data-testid="stats-card-0"]');

    // Verify initial state
    await expect(card.card).toBeVisible();

    // Click card
    await card.click();

    // Verify navigation or action triggered
    await page.waitForURL(/\/workflows|\/data/, { timeout: 5000 });
  });

  test('card hover shows tooltip', async ({ page }) => {
    await page.goto('/dashboard');

    const card = new InteractiveCard(page, '[data-testid="stats-card-0"]');

    // Hover over card
    await card.hover();

    // Verify tooltip appears
    const tooltip = page.locator('[data-testid="tooltip"]');
    await expect(tooltip).toBeVisible();
  });

  test('card expand/collapse functionality', async ({ page }) => {
    await page.goto('/dashboard');

    const card = new InteractiveCard(page, '[data-testid="expandable-card"]');

    // Expand card
    await card.expand();
    await expect(card.card).toHaveAttribute('aria-expanded', 'true');

    // Verify expanded content visible
    const expandedContent = page.locator('[data-testid="expanded-content"]');
    await expect(expandedContent).toBeVisible();

    // Collapse card
    await card.collapse();
    await expect(card.card).toHaveAttribute('aria-expanded', 'false');
  });
});
```

#### 3. Testing Button Interactions

```typescript
// specs/components/interactive-button.spec.ts
test('button shows loading state during async operation', async ({ page }) => {
  await page.goto('/workflows');

  const button = new InteractiveButton(page, 'button[data-testid="execute-workflow"]');

  // Click button
  await button.click();

  // Verify loading state
  await expect(button.isLoading()).resolves.toBe(true);

  // Wait for loading to complete
  await button.waitForLoadingComplete();

  // Verify action completed
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
});

test('disabled button does not trigger action', async ({ page }) => {
  await page.goto('/workflows');

  const button = new InteractiveButton(page, 'button[data-testid="delete-workflow"]');

  // Verify button is disabled
  await expect(button.isDisabled()).resolves.toBe(true);

  // Attempt to click (should not trigger action)
  await button.button.click({ force: true });

  // Verify no action occurred
  await expect(page.locator('[data-testid="confirmation-modal"]')).not.toBeVisible();
});
```

---

## HTMX Functionality Testing

### ✅ Best Practices

#### 1. Testing Dual-Response Pattern

```typescript
// specs/htmx/dual-response.spec.ts
import { test, expect } from '@playwright/test';

test.describe('HTMX Dual-Response Pattern', () => {
  test('HTMX request returns partial template', async ({ page }) => {
    // Set HTMX header
    await page.setExtraHTTPHeaders({
      'HX-Request': 'true',
    });

    await page.goto('/workflows');

    // Verify partial template (no base.html elements)
    const body = page.locator('body');
    await expect(body).not.toContainText('Navigation'); // Base template element

    // Verify partial content exists
    await expect(page.locator('[data-testid="workflows-content"]')).toBeVisible();
  });

  test('regular request returns full page', async ({ page }) => {
    // No HTMX header
    await page.goto('/workflows');

    // Verify full page (base.html elements present)
    await expect(page.locator('nav')).toBeVisible(); // Base template navigation
    await expect(page.locator('[data-testid="workflows-content"]')).toBeVisible();
  });
});
```

#### 2. Testing HTMX Swap Operations

```typescript
// specs/htmx/swap-operations.spec.ts
test('HTMX innerHTML swap updates content', async ({ page }) => {
  await page.goto('/dashboard');

  const refreshButton = page.locator('button[data-testid="refresh-data"]');
  const targetElement = page.locator('[data-testid="data-table"]');

  // Get initial content
  const initialContent = await targetElement.textContent();

  // Click refresh (triggers HTMX request)
  await refreshButton.click();

  // Wait for HTMX swap
  await page.waitForFunction(
    (selector) => {
      const element = document.querySelector(selector);
      return element && !element.classList.contains('htmx-swapping');
    },
    '[data-testid="data-table"]',
    { timeout: 10000 }
  );

  // Verify content updated
  const updatedContent = await targetElement.textContent();
  expect(updatedContent).not.toBe(initialContent);
});
```

#### 3. Testing HTMX Loading States

```typescript
test('HTMX shows loading indicator during request', async ({ page }) => {
  await page.goto('/workflows');

  const loadButton = page.locator('button[data-testid="load-more"]');

  // Click to trigger HTMX request
  await loadButton.click();

  // Verify loading indicator appears
  const loadingIndicator = page.locator('[data-testid="htmx-loading"]');
  await expect(loadingIndicator).toBeVisible();

  // Wait for request to complete
  await page.waitForFunction(() => {
    return !document.querySelector('.htmx-request');
  }, { timeout: 10000 });

  // Verify loading indicator disappears
  await expect(loadingIndicator).not.toBeVisible();
});
```

---

## Form Testing

### ✅ Best Practices

#### 1. Testing Form Validation

```typescript
// specs/forms/validation.spec.ts
test('form shows validation errors for required fields', async ({ page }) => {
  await page.goto('/workflows/create');

  const form = page.locator('form[data-testid="workflow-form"]');

  // Submit form without filling required fields
  await form.locator('button[type="submit"]').click();

  // Verify validation errors appear
  await expect(page.locator('[data-testid="error-name"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-name"]')).toContainText('required');

  await expect(page.locator('[data-testid="error-description"]')).toBeVisible();
});

test('form validates field formats', async ({ page }) => {
  await page.goto('/workflows/create');

  const emailInput = page.locator('input[name="email"]');

  // Enter invalid email
  await emailInput.fill('invalid-email');
  await emailInput.blur();

  // Verify format validation error
  await expect(page.locator('[data-testid="error-email"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-email"]')).toContainText('valid email');
});
```

#### 2. Testing Form Submission

```typescript
test('form submission workflow', async ({ page }) => {
  await page.goto('/workflows/create');

  // Fill form
  await page.fill('input[name="name"]', 'Test Workflow');
  await page.fill('textarea[name="description"]', 'Test description');

  // Submit form
  await page.click('button[type="submit"]');

  // Wait for HTMX request
  await page.waitForFunction(() => {
    return !document.querySelector('.htmx-request');
  }, { timeout: 10000 });

  // Verify success message
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="success-message"]')).toContainText('created successfully');

  // Verify redirect or list update
  await expect(page).toHaveURL(/\/workflows/);
  await expect(page.locator('text=Test Workflow')).toBeVisible();
});
```

#### 3. Testing Form Error Handling

```typescript
test('form handles server errors gracefully', async ({ page }) => {
  // Mock server error
  await page.route('**/api/workflows', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Internal server error' }),
    });
  });

  await page.goto('/workflows/create');

  // Fill and submit form
  await page.fill('input[name="name"]', 'Test Workflow');
  await page.click('button[type="submit"]');

  // Verify error message displayed
  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-message"]')).toContainText('error occurred');

  // Verify form data preserved
  await expect(page.locator('input[name="name"]')).toHaveValue('Test Workflow');
});
```

---

## Data Operations Testing

### ✅ Best Practices

#### 1. Testing Create Operations

```typescript
// specs/data-operations/create.spec.ts
test('create workflow operation', async ({ page }) => {
  await page.goto('/workflows');

  // Click create button
  await page.click('button[data-testid="create-workflow"]');

  // Fill creation form
  await page.fill('input[name="name"]', 'New Workflow');
  await page.fill('textarea[name="description"]', 'Workflow description');

  // Submit
  await page.click('button[type="submit"]');
  await page.waitForHTMXComplete();

  // Verify workflow created
  await expect(page.locator('text=New Workflow')).toBeVisible();

  // Verify success feedback
  await expect(page.locator('[data-testid="success-notification"]')).toBeVisible();
});
```

#### 2. Testing Update Operations

```typescript
test('update workflow operation', async ({ page }) => {
  await page.goto('/workflows');

  // Click edit button for first workflow
  await page.click('[data-testid="workflow-item-0"] button[data-testid="edit"]');

  // Update form fields
  await page.fill('input[name="name"]', 'Updated Workflow Name');

  // Save changes
  await page.click('button[data-testid="save"]');
  await page.waitForHTMXComplete();

  // Verify update reflected
  await expect(page.locator('text=Updated Workflow Name')).toBeVisible();

  // Verify success feedback
  await expect(page.locator('[data-testid="success-notification"]')).toBeVisible();
});
```

#### 3. Testing Delete Operations

```typescript
test('delete workflow with confirmation', async ({ page }) => {
  await page.goto('/workflows');

  const workflowName = await page.locator('[data-testid="workflow-item-0"]').textContent();

  // Click delete button
  await page.click('[data-testid="workflow-item-0"] button[data-testid="delete"]');

  // Verify confirmation modal appears
  await expect(page.locator('[data-testid="confirmation-modal"]')).toBeVisible();
  await expect(page.locator('[data-testid="confirmation-modal"]')).toContainText('Are you sure');

  // Confirm deletion
  await page.click('button[data-testid="confirm-delete"]');
  await page.waitForHTMXComplete();

  // Verify workflow removed from list
  if (workflowName) {
    await expect(page.locator(`text=${workflowName}`)).not.toBeVisible();
  }

  // Verify success feedback
  await expect(page.locator('[data-testid="success-notification"]')).toBeVisible();
});
```

#### 4. Testing Filtering and Searching

```typescript
test('filter workflows by status', async ({ page }) => {
  await page.goto('/workflows');

  // Select filter
  await page.selectOption('[data-testid="status-filter"]', 'active');
  await page.waitForHTMXComplete();

  // Verify only active workflows shown
  const workflowItems = page.locator('[data-testid="workflow-item"]');
  const count = await workflowItems.count();

  for (let i = 0; i < count; i++) {
    const status = await workflowItems.nth(i).locator('[data-testid="status"]').textContent();
    expect(status).toBe('active');
  }
});

test('search workflows by name', async ({ page }) => {
  await page.goto('/workflows');

  // Enter search query
  await page.fill('[data-testid="search-input"]', 'Test');
  await page.waitForHTMXComplete();

  // Verify filtered results
  const workflowItems = page.locator('[data-testid="workflow-item"]');
  const count = await workflowItems.count();

  for (let i = 0; i < count; i++) {
    const name = await workflowItems.nth(i).locator('[data-testid="name"]').textContent();
    expect(name?.toLowerCase()).toContain('test');
  }
});
```

---

## UI State & Feedback Testing

### ✅ Best Practices

#### 1. Testing Loading States

```typescript
// specs/ui-states/loading.spec.ts
test('loading state appears during data fetch', async ({ page }) => {
  await page.goto('/workflows');

  // Trigger data refresh
  await page.click('button[data-testid="refresh"]');

  // Verify loading indicator appears
  await expect(page.locator('[data-testid="loading-indicator"]')).toBeVisible();

  // Wait for loading to complete
  await page.waitForSelector('[data-testid="loading-indicator"]', {
    state: 'hidden',
    timeout: 10000,
  });

  // Verify data updated
  await expect(page.locator('[data-testid="workflow-list"]')).toBeVisible();
});
```

#### 2. Testing Success States

```typescript
test('success message appears after operation', async ({ page }) => {
  await page.goto('/workflows/create');

  // Complete form and submit
  await page.fill('input[name="name"]', 'Test Workflow');
  await page.click('button[type="submit"]');
  await page.waitForHTMXComplete();

  // Verify success message
  const successMessage = page.locator('[data-testid="success-message"]');
  await expect(successMessage).toBeVisible();
  await expect(successMessage).toContainText('created successfully');

  // Verify message auto-dismisses (if applicable)
  await page.waitForTimeout(5000);
  await expect(successMessage).not.toBeVisible();
});
```

#### 3. Testing Error States

```typescript
test('error message appears on operation failure', async ({ page }) => {
  // Mock server error
  await page.route('**/api/workflows', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' }),
    });
  });

  await page.goto('/workflows/create');

  // Submit form
  await page.fill('input[name="name"]', 'Test Workflow');
  await page.click('button[type="submit"]');
  await page.waitForHTMXComplete();

  // Verify error message
  const errorMessage = page.locator('[data-testid="error-message"]');
  await expect(errorMessage).toBeVisible();
  await expect(errorMessage).toContainText('error occurred');

  // Verify error is user-friendly
  await expect(errorMessage).not.toContainText('500');
  await expect(errorMessage).not.toContainText('Internal Server Error');
});
```

#### 4. Testing Disabled States

```typescript
test('buttons disabled when action unavailable', async ({ page }) => {
  await page.goto('/workflows');

  // Verify delete button disabled when no selection
  const deleteButton = page.locator('button[data-testid="delete-selected"]');
  await expect(deleteButton).toBeDisabled();

  // Select workflow
  await page.click('[data-testid="workflow-item-0"] input[type="checkbox"]');

  // Verify delete button enabled
  await expect(deleteButton).toBeEnabled();
});
```

---

## Visual Regression Testing

### ✅ Best Practices

#### 1. Screenshot Comparisons

```typescript
// specs/visual/regression.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('dashboard page visual consistency', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');

    // Take screenshot and compare
    await expect(page).toHaveScreenshot('dashboard.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test('workflows page visual consistency', async ({ page }) => {
    await page.goto('/workflows');
    await page.waitForLoadState('networkidle');

    await expect(page).toHaveScreenshot('workflows.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });
});
```

#### 2. Component Visual Testing

```typescript
test('interactive card visual states', async ({ page }) => {
  await page.goto('/dashboard');

  const card = page.locator('[data-testid="stats-card-0"]');

  // Default state
  await expect(card).toHaveScreenshot('card-default.png');

  // Hover state
  await card.hover();
  await expect(card).toHaveScreenshot('card-hover.png');

  // Active state
  await card.click();
  await expect(card).toHaveScreenshot('card-active.png');
});
```

---

## Accessibility Testing

### ✅ Best Practices

#### 1. Using axe-core

```typescript
// specs/accessibility/axe-core.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('dashboard page accessibility', async ({ page }) => {
  await page.goto('/dashboard');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});

test('workflows page accessibility', async ({ page }) => {
  await page.goto('/workflows');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .disableRules(['color-contrast']) // If needed for specific cases
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

#### 2. Keyboard Navigation Testing

```typescript
// specs/accessibility/keyboard-navigation.spec.ts
test('keyboard navigation through workflow list', async ({ page }) => {
  await page.goto('/workflows');

  // Tab to first workflow item
  await page.keyboard.press('Tab');
  await page.keyboard.press('Tab');

  // Verify focus on first workflow
  const firstWorkflow = page.locator('[data-testid="workflow-item-0"]');
  await expect(firstWorkflow).toBeFocused();

  // Arrow down to next workflow
  await page.keyboard.press('ArrowDown');
  const secondWorkflow = page.locator('[data-testid="workflow-item-1"]');
  await expect(secondWorkflow).toBeFocused();

  // Enter to activate
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/\/workflows\/\d+/);
});
```

#### 3. Screen Reader Testing

```typescript
test('ARIA labels and roles correct', async ({ page }) => {
  await page.goto('/workflows');

  // Verify buttons have accessible names
  const createButton = page.locator('button[data-testid="create-workflow"]');
  await expect(createButton).toHaveAttribute('aria-label');

  // Verify form inputs have labels
  const searchInput = page.locator('[data-testid="search-input"]');
  const labelId = await searchInput.getAttribute('aria-labelledby');
  expect(labelId).toBeTruthy();

  // Verify modal has proper role
  await page.click('button[data-testid="create-workflow"]');
  const modal = page.locator('[data-testid="create-modal"]');
  await expect(modal).toHaveAttribute('role', 'dialog');
  await expect(modal).toHaveAttribute('aria-labelledby');
});
```

---

## Performance Testing

### ✅ Best Practices

#### 1. Page Load Performance

```typescript
// specs/performance/load-time.spec.ts
test('dashboard page load performance', async ({ page }) => {
  const startTime = Date.now();

  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');

  const loadTime = Date.now() - startTime;

  // Verify load time within budget
  expect(loadTime).toBeLessThan(3000); // 3 seconds

  // Measure time to interactive
  const timeToInteractive = await page.evaluate(() => {
    return performance.timing.domInteractive - performance.timing.navigationStart;
  });

  expect(timeToInteractive).toBeLessThan(2000); // 2 seconds
});
```

#### 2. HTMX Partial Load Performance

```typescript
test('HTMX partial load performance', async ({ page }) => {
  await page.goto('/dashboard');

  const startTime = Date.now();

  // Trigger HTMX request
  await page.click('button[data-testid="refresh"]');

  // Wait for HTMX complete
  await page.waitForFunction(() => {
    return !document.querySelector('.htmx-request');
  }, { timeout: 10000 });

  const loadTime = Date.now() - startTime;

  // Verify partial load within budget
  expect(loadTime).toBeLessThan(1000); // 1 second
});
```

---

## Test Data Management

### ✅ Best Practices

#### 1. Test Data Factories

```typescript
// fixtures/data.fixture.ts
import { faker } from '@faker-js/faker';

export class TestDataFactory {
  static createWorkflow() {
    return {
      name: faker.company.name(),
      description: faker.lorem.paragraph(),
      steps: Array.from({ length: 3 }, () => faker.lorem.word()),
    };
  }

  static createUser() {
    return {
      username: faker.internet.userName(),
      email: faker.internet.email(),
      password: faker.internet.password(),
    };
  }
}
```

#### 2. Test Data Cleanup

```typescript
// fixtures/data.fixture.ts
export const test = base.extend({
  testWorkflow: async ({ page, baseURL }, use) => {
    // Create test workflow
    await page.goto(`${baseURL}/workflows/create`);
    const workflow = TestDataFactory.createWorkflow();
    await page.fill('input[name="name"]', workflow.name);
    await page.fill('textarea[name="description"]', workflow.description);
    await page.click('button[type="submit"]');
    await page.waitForHTMXComplete();

    await use(workflow);

    // Cleanup
    await page.goto(`${baseURL}/workflows`);
    await page.click(`[data-testid="workflow-${workflow.name}"] button[data-testid="delete"]`);
    await page.click('button[data-testid="confirm-delete"]');
    await page.waitForHTMXComplete();
  },
});
```

---

## Error Handling & Edge Cases

### ✅ Best Practices

#### 1. Network Error Handling

```typescript
// specs/errors/network-errors.spec.ts
test('handles network errors gracefully', async ({ page }) => {
  // Simulate network failure
  await page.route('**/api/workflows', route => route.abort());

  await page.goto('/workflows');

  // Trigger action that requires network
  await page.click('button[data-testid="refresh"]');

  // Verify error message displayed
  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-message"]')).toContainText('network');

  // Verify UI remains functional
  await expect(page.locator('[data-testid="workflow-list"]')).toBeVisible();
});
```

#### 2. Timeout Handling

```typescript
test('handles request timeouts', async ({ page }) => {
  // Simulate slow response
  await page.route('**/api/workflows', async route => {
    await new Promise(resolve => setTimeout(resolve, 15000)); // 15 seconds
    await route.continue();
  });

  await page.goto('/workflows');

  // Trigger action
  await page.click('button[data-testid="refresh"]');

  // Verify timeout handling
  await page.waitForTimeout(11000); // Wait for timeout

  // Verify timeout message or retry option
  await expect(
    page.locator('[data-testid="timeout-message"], [data-testid="retry-button"]')
  ).toBeVisible();
});
```

---

## CI/CD Integration

### ✅ Best Practices

#### 1. GitHub Actions Example

```yaml
# .github/workflows/playwright.yml
name: Playwright E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npx playwright test
        env:
          BASE_URL: http://localhost:8080

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

---

## Summary

### Key Principles

1. **Test User Interactions, Not Just Page Loads**: Focus on functionality, workflows, and user experience
2. **Use Page Object Model**: Encapsulate page logic for maintainability
3. **Test Component Functionality**: Verify all interactive components work correctly
4. **Test HTMX Functionality**: Validate dual-response pattern and partial updates
5. **Test Forms Comprehensively**: Validation, submission, error handling
6. **Test Data Operations**: Create, read, update, delete workflows
7. **Test UI States**: Loading, success, error, disabled states
8. **Test Accessibility**: WCAG 2.1 AA compliance
9. **Test Visual Consistency**: Visual regression testing
10. **Test Performance**: Load times and responsiveness

### Success Metrics

- ✅ 100% page coverage (all 29 pages tested)
- ✅ 100% component coverage (all 10 components tested)
- ✅ 100% navigation link coverage
- ✅ 100% form coverage
- ✅ 100% HTMX route coverage
- ✅ WCAG 2.1 AA accessibility compliance
- ✅ 0 flaky tests
- ✅ All tests complete in < 30 minutes
- ✅ Professional, enterprise-grade UX verified

---

**References**:
- [Playwright Documentation](https://playwright.dev/)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Axe-Core Playwright](https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
