# Database Schema (dbdiagram)

This document captures the proposed relational schema for the Zebras Slack framework. The DBML block below can be pasted into [dbdiagram.io](https://dbdiagram.io) or the `dbml-renderer` CLI to visualise and iterate on the design. It balances today’s implemented models with the roadmap (rules engine, invite helper, auto-join, autoresponder).

```dbml
Table event_logs {
  id int [pk, increment]
  created_at timestamptz
  event_type varchar(64)
  subtype varchar(64) [null]
  team_id varchar(32) [null]
  channel_id varchar(32) [null]
  user_id varchar(32) [null]
  message_ts varchar(32) [null]
  thread_ts varchar(32) [null]
  action varchar(64) [null]
  raw jsonb
  indexes {
    (event_type) [name: 'idx_event_logs_event_type']
    (team_id) [name: 'idx_event_logs_team_id']
    (channel_id) [name: 'idx_event_logs_channel']
    (user_id) [name: 'idx_event_logs_user']
  }
}

Table channel_rules {
  id int [pk, increment]
  channel_id varchar(32) [unique]
  allow_top_level_posts boolean [default: true]
  allow_thread_replies boolean [default: true]
  allow_bots boolean [default: true]
  updated_at timestamptz
}

Table rule_policies {
  id int [pk, increment]
  name varchar(128)
  policy_type varchar(32) [note: 'thread_lockdown | bot_block | channel_guard | custom']
  is_enabled boolean [default: true]
  severity varchar(16) [default: 'info']
  config jsonb
  created_at timestamptz
  updated_at timestamptz
  created_by varchar(32) [null]
  updated_by varchar(32) [null]
}

Table rule_policy_channels {
  id int [pk, increment]
  policy_id int [ref: > rule_policies.id]
  channel_id varchar(32)
  scope varchar(16) [default: 'include', note: 'include | exclude']
  created_at timestamptz
  indexes {
    (policy_id, channel_id) [unique, name: 'uq_rule_policy_channels']
  }
}

Table rule_exemptions {
  id int [pk, increment]
  policy_id int [ref: > rule_policies.id]
  subject_type varchar(16) [note: 'user | role | channel | usergroup']
  subject_id varchar(64)
  created_at timestamptz
  created_by varchar(32) [null]
  note text [null]
}

Table rule_violation_audits {
  id int [pk, increment]
  occurred_at timestamptz
  policy_id int [ref: > rule_policies.id]
  channel_id varchar(32)
  user_id varchar(32)
  message_ts varchar(32) [null]
  thread_ts varchar(32) [null]
  action_taken varchar(32) [note: 'delete | warn | notify | none']
  reason text
  event_log_id int [ref: > event_logs.id, null]
  audit_channel_message_ts varchar(32) [null]
  metadata jsonb [null]
}

Table invite_settings {
  id int [pk, increment]
  admin_channel_id varchar(32) [null]
  audit_channel_id varchar(32) [null]
  notify_on_join boolean [default: true]
  dm_message text [null]
  updated_at timestamptz
}

Table invite_requests {
  id int [pk, increment]
  requester_user_id varchar(32)
  invitee_email varchar(255) [null]
  invitee_user_id varchar(32) [null]
  target_channel_id varchar(32) [null]
  requested_at timestamptz
  status varchar(16) [default: 'pending', note: 'pending | approved | denied | auto']
  reviewed_by_user_id varchar(32) [null]
  reviewed_at timestamptz [null]
  reason text [null]
  metadata jsonb [null]
}

Table invite_request_actions {
  id int [pk, increment]
  request_id int [ref: > invite_requests.id]
  action_type varchar(32) [note: 'notified | dm_sent | approved | denied']
  performed_at timestamptz
  actor_user_id varchar(32) [null]
  payload jsonb [null]
}

Table auto_responder_rules {
  id int [pk, increment]
  phrase text
  response_text text
  match_type varchar(16) [note: 'contains | exact | regex']
  case_sensitive boolean [default: false]
  channel_id varchar(32) [null]
  enabled boolean [default: true]
  created_at timestamptz [null]
  updated_at timestamptz [null]
  indexes {
    (channel_id) [name: 'idx_auto_responder_channel']
  }
}

Table auto_join_configs {
  id int [pk, increment]
  channel_id varchar(32)
  target_type varchar(16) [note: 'bot | user | usergroup']
  target_id varchar(64) [null]
  is_enabled boolean [default: true]
  join_on_create boolean [default: true]
  last_joined_at timestamptz [null]
  created_at timestamptz
  updated_at timestamptz
  indexes {
    (channel_id, target_type, target_id) [unique, name: 'uq_auto_join_target']
  }
}

Table auto_join_audits {
  id int [pk, increment]
  config_id int [ref: > auto_join_configs.id]
  channel_id varchar(32)
  target_type varchar(16)
  target_id varchar(64) [null]
  status varchar(16) [note: 'success | failed | skipped']
  details text [null]
  occurred_at timestamptz
}
```

**Reference Notes**
- `event_logs` reflects the existing implementation; other tables extend roadmap functionality (rules engine persistence, invite helper workflows, auto-responder, auto-join tracking).
- `rule_policies` + join tables create a flexible rules DSL foundation while retaining `channel_rules` for the current boolean toggles.
- `invite_requests` / `invite_request_actions` enable auditability for admin approvals and notifications, with `invite_settings` covering global configuration.
- `auto_join_configs` / `auto_join_audits` track desired auto-join targets and execution history, useful for alerting on failures.
```
