from sqlalchemy.orm import Session
from typing import Optional
from backend.app.models.learning import Subject, Topic, StudySession, Note
from backend.app.models.project import Project, ProjectTask, ArchitectureDecision
from backend.app.models.growth import DailyReview
from backend.app.models.business import BusinessOpportunity, Experiment

class ContextBuilder:
    @staticmethod
    def build_system_instruction(
        db: Session,
        context_type: str = "General Mentor",
        subject_id: Optional[int] = None,
        project_id: Optional[int] = None
    ) -> str:
        base_persona = (
            "You are the personal CTO, Principal Software Architect, and strict technical mentor for Nitish, "
            "an undergraduate BTech Information Technology student (graduating 2027) aiming to become an independent "
            "SDE, AI Engineer, and Technology Founder.\n"
            "Your mentoring rules:\n"
            "- Think like a senior principal architect. Never blindly agree with lazy technical decisions.\n"
            "- If an approach is over-engineered or introduces unnecessary dependencies, challenge it.\n"
            "- Emphasize fundamentals: data structures, OS concurrency, normalized schema design, ACID guarantees, and automated testing.\n"
            "- Be direct, constructive, and technically rigorous. No empty motivational platitudes.\n"
            "- Ask Nitish to attempt the problem or state invariants before giving full answers when evaluating comprehension.\n"
        )

        injected_context = ""

        # Selective contextual injection
        if subject_id:
            sub = db.query(Subject).filter(Subject.id == subject_id).first()
            if sub:
                topics_summary = ", ".join([f"{t.title} ({t.status})" for t in sub.topics[:10]])
                recent_notes = db.query(Note).filter(Note.subject_id == subject_id).order_by(Note.updated_at.desc()).limit(3).all()
                notes_text = "\n".join([f"- Note '{n.title}': {n.content_markdown[:200]}..." for n in recent_notes])
                injected_context += (
                    f"\n[ACTIVE SUBJECT CONTEXT]:\n"
                    f"Subject: {sub.name} (Code: {sub.code}, Category: {sub.category}, Difficulty: {sub.difficulty})\n"
                    f"Topics: {topics_summary or 'No topics defined yet'}\n"
                    f"Recent Technical Notes:\n{notes_text or 'None'}\n"
                )

        if project_id:
            proj = db.query(Project).filter(Project.id == project_id).first()
            if proj:
                tasks_summary = ", ".join([f"{t.title} [{t.status}]" for t in proj.tasks[:8]])
                adrs_summary = "; ".join([f"ADR #{a.adr_number} ({a.title}): {a.decision[:100]}" for a in proj.architecture_decisions[:4]])
                injected_context += (
                    f"\n[ACTIVE PROJECT CONTEXT]:\n"
                    f"Project: {proj.name} ({proj.tagline})\n"
                    f"Local Path: {proj.local_path}\n"
                    f"Tech Stack: {proj.tech_stack_json}\n"
                    f"Active Tasks: {tasks_summary or 'None'}\n"
                    f"Architecture Decisions: {adrs_summary or 'None'}\n"
                )

        # Pull today's priority context
        today_review = db.query(DailyReview).order_by(DailyReview.review_date.desc()).first()
        if today_review:
            injected_context += (
                f"\n[CURRENT DAILY FOCUS]:\n"
                f"Priority 1: {today_review.priority_1} (Done: {today_review.priority_1_done})\n"
                f"Priority 2: {today_review.priority_2} (Done: {today_review.priority_2_done})\n"
            )

        return base_persona + injected_context

