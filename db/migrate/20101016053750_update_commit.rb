class UpdateCommit < ActiveRecord::Migration
  def self.up
    add_column :commits, :active_branch, :string
    add_column :commits, :files, :integer
    add_column :commits, :insertions, :integer
    add_column :commits, :deletions, :integer
    add_column :commits, :lines, :integer
    rename_column :commits, :author, :author_email
  end

  def self.down
    rename_column :commits, :author_email, :author
    remove_column :commits, :lines
    remove_column :commits, :deletions
    remove_column :commits, :insertions
    remove_column :commits, :files
    remove_column :commits, :active_branch
  end
end
