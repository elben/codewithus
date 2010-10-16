# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended to check this file into your version control system.

ActiveRecord::Schema.define(:version => 20101016084841) do

  create_table "commits", :force => true do |t|
    t.string   "author_email"
    t.text     "message"
    t.string   "commit_hash"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "active_branch"
    t.integer  "files"
    t.integer  "insertions"
    t.integer  "deletions"
  end

  create_table "events", :force => true do |t|
    t.integer  "user_id"
    t.string   "kind"
    t.integer  "data_id"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.integer  "time"
  end

  create_table "subscriptions", :force => true do |t|
    t.integer  "user_id"
    t.integer  "subscribee_id"
    t.integer  "latest"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "users", :force => true do |t|
    t.string   "email"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "name"
  end

end
