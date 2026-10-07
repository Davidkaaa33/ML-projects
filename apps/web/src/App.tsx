import { MLSystemsLab } from "./Lab";
import {
  capabilities,
  featuredProjects,
  profile,
  profileName
} from "./portfolio";

function ExternalLinks({ compact = false }: { compact?: boolean }) {
  const links = [
    { label: "GitHub", href: profile.github },
    { label: "LinkedIn", href: profile.linkedin },
    { label: "Resume", href: profile.resume }
  ].filter((link) => link.href);

  return (
    <div className={compact ? "external-links compact" : "external-links"}>
      {links.map((link) => (
        <a key={link.label} href={link.href} target="_blank" rel="noreferrer">
          {link.label}
        </a>
      ))}
    </div>
  );
}

function App() {
  const aboutFacts = [
    { label: "Education", value: profile.education },
    { label: "Location", value: profile.location },
    { label: "Current status", value: profile.currentStatus },
    {
      label: "Target roles",
      value: profile.targetRoles.length ? profile.targetRoles.join(" · ") : ""
    }
  ].filter((item) => item.value);

  return (
    <div className="portfolio-shell">
      <header className="portfolio-header">
        <a className="portfolio-name" href="#overview" aria-label="Back to overview">
          {profileName}
        </a>

        <nav className="portfolio-nav" aria-label="Portfolio navigation">
          <a href="#overview">Overview</a>
          <a href="#about">About</a>
          <a href="#projects">Projects</a>
          <a href="#lab">ML Systems Lab</a>
        </nav>

        <ExternalLinks compact />
      </header>

      <main>
        <section className="hero-section" id="overview">
          <div className="hero-primary">
            <p className="hero-role">{profile.role}</p>
            <h1>{profileName}</h1>
            <p className="hero-summary">{profile.summary}</p>

            <div className="hero-actions">
              <a className="primary-action" href="#projects">
                View Projects
              </a>
              <a className="secondary-action" href="#lab">
                Open ML Systems Lab
              </a>
            </div>

            <ExternalLinks />
          </div>

          <aside className="hero-evidence" aria-label="Portfolio highlights">
            <a href="#projects" className="hero-evidence-row">
              <span>Flagship</span>
              <strong>Avito Candidate Retrieval</strong>
              <em>Recall@50 0.8316</em>
            </a>
            <a href="#lab" className="hero-evidence-row">
              <span>Engineering</span>
              <strong>ML Systems Lab</strong>
              <em>5 evaluated systems</em>
            </a>
            <a href="#projects" className="hero-evidence-row">
              <span>Retrieval / RAG</span>
              <strong>Knowledge Assistant</strong>
              <em>Hit@3 100% · MRR@3 0.9091</em>
            </a>
          </aside>
        </section>

        <section className="portfolio-section about-section" id="about">
          <div className="section-heading">
            <p className="section-kicker">About me</p>
            <h2>Building ML systems beyond notebooks.</h2>
          </div>

          <div className="about-layout">
            <p className="about-copy">
              I’m a second-year BSc student in Data Analysis and Artificial Intelligence
              at Innopolis University, with a 4.9/5.0 GPA. I’m focused on ML Engineering,
              NLP and information retrieval, and on building ML projects beyond notebooks —
              with evaluation, APIs, testing and deployment.
            </p>

            {aboutFacts.length > 0 && (
              <dl className="about-facts">
                {aboutFacts.map((fact) => (
                  <div key={fact.label}>
                    <dt>{fact.label}</dt>
                    <dd>{fact.value}</dd>
                  </div>
                ))}
              </dl>
            )}
          </div>
        </section>

        <section className="portfolio-section selected-work" id="projects">
          <div className="section-heading">
            <p className="section-kicker">Selected work</p>
            <h2>Projects with measured results.</h2>
            <p>
              Retrieval, applied ML and serving-oriented systems. Metrics are
              reported from the project evaluation artifacts rather than demo sessions.
            </p>
          </div>

          <div className="project-list">
            {featuredProjects.map((project, index) => (
              <article className="featured-project" key={project.id}>
                <div className="project-index">0{index + 1}</div>

                <div className="project-main">
                  <div className="project-title-row">
                    <h3>{project.title}</h3>
                    {project.label && <span className="project-label">{project.label}</span>}
                  </div>
                  <p className="project-description">{project.description}</p>

                  <dl className="project-case">
                    <div>
                      <dt>Problem</dt>
                      <dd>{project.problem}</dd>
                    </div>
                    <div>
                      <dt>Approach</dt>
                      <dd>{project.approach}</dd>
                    </div>
                    <div>
                      <dt>Engineering</dt>
                      <dd>{project.engineering.join(" · ")}</dd>
                    </div>
                  </dl>

                  <div className="project-tech">{project.technologies.join(" · ")}</div>

                  <div className="project-actions">
                    {project.liveUrl && (
                      <a href={project.liveUrl}>
                        {project.id === "systems-lab" ? "Open Lab" : "Open in Lab"}
                      </a>
                    )}
                    {project.sourceUrl && (
                      <a href={project.sourceUrl} target="_blank" rel="noreferrer">
                        View Source
                      </a>
                    )}
                  </div>
                </div>

                <div className="project-results" aria-label={`${project.title} results`}>
                  <span>Result</span>
                  {project.metrics.map((metric) => (
                    <div key={metric.label}>
                      <strong>{metric.value}</strong>
                      <em>{metric.label}</em>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="portfolio-section engineering-section">
          <div className="section-heading">
            <p className="section-kicker">Engineering</p>
            <h2>Beyond model training.</h2>
            <p>
              The portfolio is structured around evaluation, serving and reproducibility,
              not only notebook-level experiments.
            </p>
          </div>

          <div className="capability-grid">
            {capabilities.map((capability) => (
              <div className="capability-group" key={capability.title}>
                <h3>{capability.title}</h3>
                <ul>
                  {capability.items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        <MLSystemsLab />

      </main>

      <footer className="portfolio-footer">
        <span>Built with React, FastAPI and Docker.</span>
        <div>
          <a href={profile.github} target="_blank" rel="noreferrer">GitHub</a>
          {profile.linkedin && (
            <a href={profile.linkedin} target="_blank" rel="noreferrer">LinkedIn</a>
          )}
          {profile.email && <a href={`mailto:${profile.email}`}>Email</a>}
          {profile.resume && (
            <a href={profile.resume} target="_blank" rel="noreferrer">Resume</a>
          )}
        </div>
      </footer>
    </div>
  );
}

export default App;
