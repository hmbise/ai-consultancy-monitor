"""
Change detection service for tracking signal changes over time.
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.signal_scanner.models.signal import Signal, SignalType


class ChangeType(str, Enum):
    NEW_SIGNAL = "new_signal"
    SIGNAL_REMOVED = "signal_removed"
    SIGNAL_INTENSITY = "signal_intensity"
    CROSS_SIGNAL = "cross_signal"


class ChangeEvent(BaseModel):
    change_type: ChangeType
    company_id: UUID
    signal_type: Optional[SignalType] = None
    severity: str  # low, medium, high, critical
    description: str
    related_signals: List[UUID]
    detected_at: datetime


class ChangeDetector:
    """Detects changes in signal patterns for companies."""

    def __init__(self, signal_store: Any):
        self.signal_store = signal_store
        self.intensity_threshold = 3  # Number of signals to trigger intensity alert
        self.intensity_window_days = 30

    async def detect_changes(
        self,
        company_id: UUID,
        new_signals: List[Signal],
    ) -> List[ChangeEvent]:
        """
        Detect changes by comparing new signals with existing ones.
        
        Args:
            company_id: Company ID to check
            new_signals: Newly discovered signals
            
        Returns:
            List of change events
        """
        changes = []

        # Get existing active signals for company
        existing_signals = await self._get_existing_signals(company_id)

        # Check for new signals
        for signal in new_signals:
            if not self._signal_exists(signal, existing_signals):
                changes.append(
                    ChangeEvent(
                        change_type=ChangeType.NEW_SIGNAL,
                        company_id=company_id,
                        signal_type=signal.signal_type,
                        severity="medium",
                        description=f"New {signal.signal_type.value} signal detected",
                        related_signals=[signal.id],
                        detected_at=datetime.utcnow(),
                    )
                )

        # Check for signal intensity
        intensity_changes = await self._check_signal_intensity(company_id, new_signals)
        changes.extend(intensity_changes)

        # Check for cross-signal patterns
        cross_signal = await self._check_cross_signal(company_id, new_signals)
        if cross_signal:
            changes.append(cross_signal)

        return changes

    async def _get_existing_signals(self, company_id: UUID) -> List[Signal]:
        """Fetch existing signals for a company."""
        # Implementation would query the signal store
        return []

    def _signal_exists(
        self,
        new_signal: Signal,
        existing_signals: List[Signal],
    ) -> bool:
        """Check if a similar signal already exists."""
        for existing in existing_signals:
            if (
                existing.signal_type == new_signal.signal_type
                and existing.source == new_signal.source
                and self._is_similar_content(existing.title, new_signal.title)
            ):
                return True
        return False

    def _is_similar_content(self, text1: str, text2: str, threshold: float = 0.8) -> bool:
        """Check if two text strings are similar using simple overlap."""
        # Simple similarity check - in production, use proper fuzzy matching
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return False
            
        intersection = words1 & words2
        union = words1 | words2
        
        similarity = len(intersection) / len(union)
        return similarity >= threshold

    async def _check_signal_intensity(
        self,
        company_id: UUID,
        new_signals: List[Signal],
    ) -> List[ChangeEvent]:
        """
        Check if there are multiple signals of the same type within the window.
        
        Returns:
            List of intensity change events
        """
        changes = []
        cutoff_date = datetime.utcnow() - timedelta(days=self.intensity_window_days)

        # Group signals by type
        signals_by_type: Dict[SignalType, List[Signal]] = {}
        for signal in new_signals:
            if signal.signal_type not in signals_by_type:
                signals_by_type[signal.signal_type] = []
            signals_by_type[signal.signal_type].append(signal)

        # Check for intensity in each category
        for signal_type, signals in signals_by_type.items():
            recent_signals = [
                s for s in signals
                if s.discovered_at > cutoff_date
            ]

            if len(recent_signals) >= self.intensity_threshold:
                changes.append(
                    ChangeEvent(
                        change_type=ChangeType.SIGNAL_INTENSITY,
                        company_id=company_id,
                        signal_type=signal_type,
                        severity="high",
                        description=(
                            f"High intensity: {len(recent_signals)} {signal_type.value} "
                            f"signals in {self.intensity_window_days} days"
                        ),
                        related_signals=[s.id for s in recent_signals],
                        detected_at=datetime.utcnow(),
                    )
                )

        return changes

    async def _check_cross_signal(
        self,
        company_id: UUID,
        new_signals: List[Signal],
    ) -> Optional[ChangeEvent]:
        """
        Check if there are signals across multiple categories (indicating broad organizational change).
        
        Returns:
            Cross-signal change event if detected, None otherwise
        """
        # Define cross-signal categories that indicate significant change
        cross_categories = {
            "hiring": [
                SignalType.HIRING_FINANCE_LEAD,
                SignalType.HIRING_OPS_LEAD,
                SignalType.HIRING_DATA_LEAD,
                SignalType.HIRING_LEGAL_LEAD,
            ],
            "funding": [
                SignalType.FUNDING_ANNOUNCED,
                SignalType.FUNDING_STAGE_CHANGE,
            ],
            "operational": [
                SignalType.LEADERSHIP_CHANGE,
                SignalType.OFFICE_EXPANSION,
                SignalType.NEW_PRODUCT,
            ],
        }

        # Check which categories have signals
        signals_by_category = {cat: [] for cat in cross_categories}
        for signal in new_signals:
            for category, types in cross_categories.items():
                if signal.signal_type in types:
                    signals_by_category[category].append(signal)

        # If signals in 2+ categories, it's a cross-signal event
        active_categories = [
            cat for cat, signals in signals_by_category.items() if signals
        ]

        if len(active_categories) >= 2:
            all_signals = []
            for signals in signals_by_category.values():
                all_signals.extend(signals)

            return ChangeEvent(
                change_type=ChangeType.CROSS_SIGNAL,
                company_id=company_id,
                severity="critical",
                description=(
                    f"Cross-signal detected: signals in {', '.join(active_categories)}. "
                    "Indicates significant organizational change."
                ),
                related_signals=[s.id for s in all_signals],
                detected_at=datetime.utcnow(),
            )

        return None
