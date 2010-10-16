class RemoveLinesFromCommits < ActiveRecord::Migration
  def self.up
    remove_column :commits, :lines
  end

  def self.down
    add_column :commits, :lines, :integer
  end
end
